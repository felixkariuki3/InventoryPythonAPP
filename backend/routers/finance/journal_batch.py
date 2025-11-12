from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from backend.dependencies import get_db
from backend.models.finance.accounting import JournalEntry
from backend.models.finance.journal_batch import JournalBatch
from backend.services.finance.journal_entry import post_journal_batch
from backend.services.finance.journal_batch_service import create_journal_batch
from backend.schemas.finance.journal_entry import JournalEntryRead, PostJournalBatchResponse

router = APIRouter(
    prefix="/batches",
    tags=["Journal Batches"]
)


# ---------------------------------------------------------------------
# 1️⃣ Create Batch
# ---------------------------------------------------------------------
@router.post("/", response_model=dict)
def create_batch(
    source_module: str,
    description: str,
    db: Session = Depends(get_db)
):
    """
    Create a new journal batch.
    """
    try:
        batch = create_journal_batch(db, source_module, description)
        return {"message": "Batch created successfully", "batch_no": batch.batch_no, "id": batch.id}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail={str(e)})


# ---------------------------------------------------------------------
# 2️⃣ List All Batches
# ---------------------------------------------------------------------
@router.get("/", response_model=List[dict])
def list_batches(db: Session = Depends(get_db)):
    """
    Retrieve all journal batches.
    """
    batches = db.query(JournalBatch).all()
    return [
        {
            "id": b.id,
            "batch_no": b.batch_no,
            "source_module": b.source_module,
            "description": b.description,
            "status": b.status,
            "created_at": b.created_at,
            "posted_at": b.posted_at
        }
        for b in batches
    ]


# ---------------------------------------------------------------------
# 3️⃣ Get Entries by Batch
# ---------------------------------------------------------------------
@router.get("/{batch_id}/entries", response_model=List[JournalEntryRead])
def get_batch_entries(batch_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all journal entries in a specific batch.
    """
    entries = db.query(JournalEntry).filter(JournalEntry.batch_no == batch_id).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No entries found for this batch")
    return entries


# ---------------------------------------------------------------------
# 4️⃣ Post a Batch
# ---------------------------------------------------------------------
@router.post("/journal-batch/{batch_id}/post", response_model=PostJournalBatchResponse)
def api_post_journal_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = post_journal_batch(db, batch_id)
    return {"message": f"Batch {batch.batch_no} posted successfully", "batch": batch}
