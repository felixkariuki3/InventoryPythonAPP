from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from pytest import Session
from backend.models.finance.accounting import AccountingEvent, JournalEntry


def post_journal_entry(db: Session, entry_id: int):
    """
    Posts a journal entry:
    - Validates that debits == credits
    - Marks the journal as 'posted'
    - Creates an AccountingEvent record for tracking
    """
    db_entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")

    if db_entry.status == "posted":
        raise HTTPException(status_code=400, detail="Entry already posted")

    # Validation: totals
    total_debit = db_entry.total_debit or 0
    total_credit = db_entry.total_credit or 0

    if round(total_debit, 2) != round(total_credit, 2):
        raise HTTPException(
            status_code=400,
            detail=f"Unbalanced entry cannot be posted: Debit {total_debit} != Credit {total_credit}",
        )

    # Create Accounting Event (batch summary)
    event = AccountingEvent(
        batch_no=db_entry.batch_no,
        source_module="GENERAL_LEDGER",
        reference_id=db_entry.id,
        reference_table="journal_entries",
        description=db_entry.description,
        amount=total_debit,
        debit_account=None,  # optional, since we have detailed lines
        credit_account=None,
        status="posted",
        created_at=db_entry.entry_date,
        posted_at=datetime.utcnow(),
    )
    db.add(event)

    # Update journal status
    db_entry.status = "posted"

    try:
        db.commit()
        db.refresh(db_entry)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error posting journal entry: {str(e)}")

    return {"message": f"Journal Entry {db_entry.entry_number} posted successfully", "id": db_entry.id}
