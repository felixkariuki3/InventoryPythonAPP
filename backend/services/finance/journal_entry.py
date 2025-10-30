from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import date

from backend.models.finance.accounting import JournalEntry, JournalLine
from backend.models.finance.finance import Account
from backend.schemas.finance.journal_entry import (
    JournalEntryCreate,
    JournalLineCreate,
    JournalEntryUpdate,
)


# --------------------------------------------------------
# Helper: Generate Sequential Entry Number
# --------------------------------------------------------
def generate_entry_number(db: Session) -> str:
    """Auto-generate a unique entry number based on date and count."""
    today = date.today().strftime("%Y%m%d")
    count = db.query(JournalEntry).filter(JournalEntry.entry_date == date.today()).count()
    return f"JE-{today}-{count + 1:04d}"


# --------------------------------------------------------
# Create Journal Entry
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

    # Prepare entry
    db_entry = JournalEntry(
        batch_no=entry_in.batch_no,
        entry_number=entry_in.entry_number or generate_entry_number(db),
        entry_date=entry_in.entry_date,
        description=entry_in.description,
        total_debit=total_debit,
        total_credit=total_credit,
        status="draft",
    )

    db.add(db_entry)
    db.flush()  # Get entry ID before adding lines

    # Add lines
    for line in entry_in.lines:
        # Optional: Validate account existence
        account = db.query(Account).filter(Account.id == line.account_id).first()
        if not account:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid account_id: {line.account_id}",
            )

        db_line = JournalLine(
            entry_id=db_entry.id,
            account_id=line.account_id,
            description=line.description,
            debit=line.debit,
            credit=line.credit,
        )
        db.add(db_line)

    # Commit safely
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
def update_journal_entry(db: Session, entry_id: int, entry_in: JournalEntryUpdate):
    db_entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")

    # Update simple fields
    if entry_in.description is not None:
        db_entry.description = entry_in.description
    if entry_in.status is not None:
        db_entry.status = entry_in.status

    if entry_in.lines is not None:
        # Delete old lines
        db.query(JournalLine).filter(JournalLine.entry_id == db_entry.id).delete()

        # Recalculate totals
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
            account = db.query(Account).filter(Account.id == line.account_id).first()
            if not account:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid account_id: {line.account_id}",
                )

            db_line = JournalLine(
                entry_id=db_entry.id,
                account_id=line.account_id,
                description=line.description,
                debit=line.debit,
                credit=line.credit,
            )
            db.add(db_line)

    # Commit safely
    try:
        db.commit()
        db.refresh(db_entry)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return db_entry
