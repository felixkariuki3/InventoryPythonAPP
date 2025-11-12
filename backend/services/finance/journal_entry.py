from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from backend.models.finance.accounting import (
    JournalEntry,
    JournalLine
)
from backend.models.finance.journal_batch import JournalBatch
from backend.models.finance.finance import Account
from backend.schemas.finance.journal_entry import (
    JournalEntryCreate,
    JournalLineCreate,
    JournalEntryRead
)
from backend.services.finance.journal_batch_service import create_journal_batch

# --------------------------------------------------------
# Helper: Generate Sequential Entry Number
# --------------------------------------------------------
def generate_entry_number(db: Session) -> str:
    """Auto-generate a unique entry number based on date and count."""
    today = date.today().strftime("%Y%m%d")
    count = db.query(JournalEntry).filter(JournalEntry.entry_date == date.today()).count()
    return f"JE-{today}-{count + 1:04d}"


# --------------------------------------------------------
# Helper: Auto-create a Journal Batch
# --------------------------------------------------------
# def create_journal_batch(db: Session, source_module: str, description: str):
#     """Automatically create a journal batch if none exists."""
#     try:
#         batch = JournalBatch(
#             batch_no=f"{source_module[:3].upper()}-{int(datetime.utcnow().timestamp())}",
#             source_module=source_module,
#             description=description,
#             status="draft",
#             created_at=datetime.utcnow(),
#         )
#         db.add(batch)
#         db.commit()
#         db.refresh(batch)
#         return batch
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Error creating journal batch: {str(e)}")


# --------------------------------------------------------
# Create Journal Entry (with optional auto-batch)
# --------------------------------------------------------
def create_journal_entry(db: Session, entry_in: JournalEntryCreate):
    # Calculate totals
    total_debit = sum([line.debit for line in entry_in.lines])
    total_credit = sum([line.credit for line in entry_in.lines])

    if total_debit != total_credit:
        raise HTTPException(
            status_code=400,
            detail=f"Unbalanced entry: Debit {total_debit} != Credit {total_credit}",
        )

    # Auto-create a batch if not provided
    if not entry_in.batch_id:
        batch = create_journal_batch(
            db=db,
            source_module="GENERAL_LEDGER",
            description=entry_in.description or "Auto-created batch",
        )
        batch_id = batch.id
    else:
        batch_id = entry_in.batch_id

    # Prepare entry
    db_entry = JournalEntry(
        batch_no=batch_id,
        entry_number=generate_entry_number(db),
        entry_date=entry_in.entry_date or date.today(),
        description=entry_in.description,
        total_debit=total_debit,
        total_credit=total_credit,
        status="draft",
    )

    db.add(db_entry)
    db.flush()  # Get entry ID before adding lines

    # Add lines
    for line in entry_in.lines:
        account = db.query(Account).filter(Account.id == line.account_id).first()
        if not account:
            raise HTTPException(status_code=400, detail=f"Invalid account_id: {line.account_id}")

        db_line = JournalLine(
            entry_id=db_entry.id,
            account_id=line.account_id,
            description=line.description,
            debit=line.debit,
            credit=line.credit,
        )
        db.add(db_line)

    try:
        db.commit()
        db.refresh(db_entry)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return db_entry


# --------------------------------------------------------
# Update Journal Entry
# --------------------------------------------------------
def update_journal_entry(db: Session, entry_id: int, entry_in: JournalEntryRead):
    db_entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")

    # Update simple fields
    if entry_in.description is not None:
        db_entry.description = entry_in.description
    if entry_in.status is not None:
        db_entry.status = entry_in.status

    if entry_in.lines is not None:
        db.query(JournalLine).filter(JournalLine.entry_id == db_entry.id).delete()

        total_debit = sum([line.debit for line in entry_in.lines])
        total_credit = sum([line.credit for line in entry_in.lines])

        if total_debit != total_credit:
            raise HTTPException(
                status_code=400,
                detail=f"Unbalanced entry: Debit {total_debit} != Credit {total_credit}",
            )

        db_entry.total_debit = total_debit
        db_entry.total_credit = total_credit

        for line in entry_in.lines:
            account = db.query(Account).filter(Account.code == line.account_id).first()
            if not account:
                raise HTTPException(status_code=400, detail=f"Invalid account_id: {line.account_id}")

            db_line = JournalLine(
                entry_id=db_entry.id,
                account_id=line.account_id,
                description=line.description,
                debit=line.debit,
                credit=line.credit,
            )
            db.add(db_line)

    try:
        db.commit()
        db.refresh(db_entry)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return db_entry
# --------------------------------------------------------
# Helper: Check if all entries in batch are posted
# --------------------------------------------------------
def check_batch_posting_status(db: Session, batch_id: int):
    """
    Check if all journal entries in a batch are posted.
    If true, mark the batch as posted.
    """

    batch = db.query(JournalBatch).filter(JournalBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    entries = db.query(JournalEntry).filter(JournalEntry.batch_no == batch_id).all()
    if not entries:
        raise HTTPException(status_code=400, detail="No journal entries found in this batch")

    all_posted = all(entry.status == "posted" for entry in entries)

    if all_posted and batch.status != "posted":
        batch.status = "posted"
        batch.posted_at = datetime.utcnow()
        db.commit()

    return {"batch_id": batch.id, "status": batch.status}


# --------------------------------------------------------
# Post a single Journal Entry (and update batch)
# --------------------------------------------------------
def post_journal_entry(db: Session, entry_id: int):
    """
    Post a journal entry:
    - Validates debit/credit balance
    - Marks entry as posted
    - Automatically updates batch status if all entries posted
    """
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")

    if entry.status == "posted":
        raise HTTPException(status_code=400, detail="Entry already posted")

    # Validate totals
    if round(entry.total_debit or 0, 2) != round(entry.total_credit or 0, 2):
        raise HTTPException(
            status_code=400,
            detail=f"Unbalanced entry: Debit {entry.total_debit} != Credit {entry.total_credit}",
        )

    entry.status = "posted"
    db.commit()

    # Check and update batch status
    check_batch_posting_status(db, entry.batch_no)

    return {"message": f"Journal entry {entry.entry_number} posted", "status": "posted"}


# --------------------------------------------------------
# Post entire Journal Batch
# --------------------------------------------------------
def post_journal_batch(db: Session, batch_id: int):
    """
    Posts all draft entries within a batch and marks batch as posted.
    """

    batch = db.query(JournalBatch).filter(JournalBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    entries = db.query(JournalEntry).filter(JournalEntry.batch_no == batch_id).all()
    if not entries:
        raise HTTPException(status_code=400, detail="No journal entries in this batch")

    for entry in entries:
        if entry.status != "posted":
            if round(entry.total_debit or 0, 2) != round(entry.total_credit or 0, 2):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unbalanced entry {entry.entry_number}: Debit {entry.total_debit} != Credit {entry.total_credit}",
                )
            entry.status = "posted"

    batch.status = "posted"
    batch.posted_at = datetime.utcnow()

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error posting batch: {str(e)}")

    return {"batch_id": batch.id, "message": "Batch posted successfully"}