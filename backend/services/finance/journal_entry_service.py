from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from pytest import Session
from backend.models.finance.accounting import AccountingEvent, JournalEntry
from backend.services.finance.journal_entry import check_batch_posting_status


def post_journal_entry(db: Session, entry_id: int) -> JournalEntry:
    """
    Posts a single journal entry:
    - Validates debit/credit balance
    - Marks entry as posted
    - Updates batch status if all entries posted
    """
    entry: JournalEntry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
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

    # Mark entry posted
    entry.status = "posted"
    db.commit()
    db.refresh(entry)

    # Update batch status automatically
    check_batch_posting_status(db, entry.batch_no)

    return entry