# backend/services/finance/journal_batch_service.py
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from backend.models.finance.accounting import JournalEntry
from backend.models.finance.journal_batch import JournalBatch

def create_journal_batch(db: Session, source_module: str, description: str):
    """Auto-create a new journal batch."""
    try:
        batch = JournalBatch(
            batch_no=f"{source_module[:3].upper()}-{int(datetime.utcnow().timestamp())}",
            source_module=source_module,
            description=description,
            status="draft",
            created_at=datetime.utcnow(),
        )
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating journal batch: {str(e)}")


def post_journal_batch(db: Session, batch_id: int) -> JournalBatch:
    """
    Posts all draft entries in a batch and marks the batch as posted.
    """
    batch: JournalBatch = db.query(JournalBatch).filter(JournalBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    entries: list[JournalEntry] = db.query(JournalEntry).filter(JournalEntry.batch_no == batch_id).all()
    if not entries:
        raise HTTPException(status_code=400, detail="No journal entries in this batch")

    for entry in entries:
        if entry.status != "posted":
            # Validate totals
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
        db.refresh(batch)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error posting batch: {str(e)}")

    return batch