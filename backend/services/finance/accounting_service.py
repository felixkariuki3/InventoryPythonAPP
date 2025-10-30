from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.models.finance.accounting import AccountingEvent, JournalEntry, JournalLine
from backend.models.finance.finance import Account


def create_accounting_event(
    db: Session,
    source_module: str,
    reference_table: str,
    reference_id: int,
    description: str,
    amount: float,
    debit_account_id: int,
    credit_account_id: int,
):
    """
    Creates an AccountingEvent and the corresponding JournalEntry and JournalLines.
    """

    try:
        # --- 1. Create the Accounting Event (Batch) ---
        event = AccountingEvent(
            batch_no=f"{source_module[:3].upper()}-{int(datetime.utcnow().timestamp())}",
            source_module=source_module,
            reference_table=reference_table,
            reference_id=reference_id,
            description=description,
            amount=amount,
            debit_account=debit_account_id,
            credit_account=credit_account_id,
            status="draft",
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        # --- 2. Create the Journal Entry ---
        entry = JournalEntry(
            batch_no=event.id,
            entry_number=f"JE-{event.id}",
            entry_date=date.today(),
            description=description,
            total_debit=amount,
            total_credit=amount,
            status="draft",
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)

        # --- 3. Create Journal Lines (Debit and Credit) ---
        debit_line = JournalLine(
            entry_id=entry.id,
            account_id=debit_account_id,
            description=f"Debit {description}",
            debit=amount,
            credit=0,
        )
        credit_line = JournalLine(
            entry_id=entry.id,
            account_id=credit_account_id,
            description=f"Credit {description}",
            debit=0,
            credit=amount,
        )

        db.add_all([debit_line, credit_line])
        db.commit()

        return {"status": "success", "event_id": event.id, "entry_id": entry.id}

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error creating accounting event: {e}")


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
    return {"status": "posted", "entry_number": entry.entry_number}


def reverse_journal_entry(db: Session, entry_id: int):
    """
    Reverses a posted journal entry by creating a new opposite entry.
    """
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise Exception(f"Journal entry {entry_id} not found.")
    if entry.status != "posted":
        raise Exception(f"Only posted entries can be reversed.")

    reversed_entry = JournalEntry(
        batch_no=entry.batch_no,
        entry_number=f"{entry.entry_number}-REV",
        entry_date=date.today(),
        description=f"Reversal of {entry.entry_number}",
        total_debit=entry.total_credit,
        total_credit=entry.total_debit,
        status="posted",
    )
    db.add(reversed_entry)
    db.commit()
    db.refresh(reversed_entry)

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
    db.commit()
    return {"status": "reversed", "entry_number": reversed_entry.entry_number}
