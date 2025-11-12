from datetime import date, datetime
from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.models.finance.accounting import AccountingEvent, JournalEntry, JournalLine
from backend.models.finance.finance import Account
from backend.services.finance.journal_batch_service import create_journal_batch
from backend.services.finance.journal_entry import check_batch_posting_status, generate_entry_number


def create_accounting_event(
    db: Session,
    source_module: str,
    reference_table: str,
    reference_id: int,
    description: str,
    amount: float,
    debit_account: int,
    credit_account: int,
) -> AccountingEvent:
    """
    Creates an AccountingEvent, a JournalEntry, and corresponding JournalLines.
    Ensures all entries belong to a batch.
    """
    # --- 1. Create Accounting Event ---
    try:
        event = AccountingEvent(
            batch_no=f"{source_module[:3].upper()}-{int(datetime.utcnow().timestamp())}",
            source_module=source_module,
            reference_table=reference_table,
            reference_id=reference_id,
            description=description,
            amount=amount,
            debit_account=debit_account,
            credit_account=credit_account,
            currency="KES",
            status="draft",
        )
        db.add(event)
        db.commit()
        db.refresh(event)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating accounting event: {str(e)}")

    # --- 2. Ensure a Batch exists ---
    batch = create_journal_batch(
        db=db,
        source_module=source_module,
        description=f"{description} (auto-batch)"
    )

    # --- 3. Create Journal Entry ---
    entry = JournalEntry(
        batch_no=batch.id,
        entry_number=generate_entry_number(db),
        entry_date=date.today(),
        description=description,
        total_debit=amount,
        total_credit=amount,
        status="draft",
    )
    db.add(entry)
    db.flush()  # Get entry ID

    # --- 4. Create Journal Lines ---
    debit_line = JournalLine(
        entry_id=entry.id,
        account_id=debit_account,
        description=f"Debit {description}",
        debit=amount,
        credit=0,
    )
    credit_line = JournalLine(
        entry_id=entry.id,
        account_id=credit_account,
        description=f"Credit {description}",
        debit=0,
        credit=amount,
    )
    db.add_all([debit_line, credit_line])

    try:
        db.commit()
        db.refresh(entry)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating journal entry: {str(e)}")

    return event

def validate_journal_entry(db: Session, entry_id: int) -> bool:
    """
    Validates that total debits equal total credits for a journal entry.
    """
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise Exception(f"Journal entry {entry_id} not found.")

    debit_total = sum(line.debit for line in entry.lines)
    credit_total = sum(line.credit for line in entry.lines)

    if round(debit_total, 2) != round(credit_total, 2):
        raise Exception(
            f"Unbalanced entry {entry.entry_number}: Debits ({debit_total}) ≠ Credits ({credit_total})"
        )

    return True


def post_journal_entry(db: Session, entry_id: int):
    """
    Posts the journal entry (validates balance and marks as posted).
    """
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise Exception(f"Journal entry {entry_id} not found.")

    # Validate balance before posting
    validate_journal_entry(db, entry_id)

    # Mark as posted
    entry.status = "posted"
    entry.batch.status = "posted"
    entry.batch.posted_at = datetime.utcnow()

    db.commit()
    return entry


def reverse_journal_entry(db: Session, entry_id: int) -> JournalEntry:
    """
    Reverses a posted journal entry by creating a new opposite entry.
    """
    entry: JournalEntry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail=f"Journal entry {entry_id} not found")
    if entry.status != "posted":
        raise HTTPException(status_code=400, detail="Only posted entries can be reversed")

    # Create the reversed entry
    reversed_entry = JournalEntry(
        batch_no=entry.batch_no,
        entry_number=f"{entry.entry_number}-REV",
        entry_date=date.today(),
        description=f"Reversal of {entry.entry_number}",
        total_debit=entry.total_credit,
        total_credit=entry.total_debit,
        status="posted",  # Immediately posted
    )
    db.add(reversed_entry)
    db.flush()  # Get ID

    # Reverse each line
    reversed_lines = []
    for line in entry.lines:
        reversed_lines.append(
            JournalLine(
                entry_id=reversed_entry.id,
                account_id=line.account_id,
                description=f"Reversal: {line.description}",
                debit=line.credit,
                credit=line.debit,
            )
        )
    db.add_all(reversed_lines)

    # Commit and refresh
    try:
        db.commit()
        db.refresh(reversed_entry)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error reversing entry: {str(e)}")

    # Update batch status automatically
    check_batch_posting_status(db, reversed_entry.batch_no)

    return reversed_entry