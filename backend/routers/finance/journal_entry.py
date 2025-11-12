# backend/routers/finance/journal_entry_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.dependencies import get_db
from backend.schemas.finance.journal_entry import JournalEntryCreate, JournalEntryRead, JournalEntryUpdate
from backend.services.finance.journal_entry import (
    create_journal_entry,
    post_journal_entry,
    update_journal_entry
)
from backend.models.finance.accounting import JournalEntry
from backend.schemas.finance.journal_entry import (
    PostJournalEntryResponse,
    PostJournalBatchResponse,
    JournalBatchRead
)

router = APIRouter(
    prefix="/journals",
    tags=["Journal Entries"]
)

# --------------------------------------------------------
# Create a new journal entry
# --------------------------------------------------------
@router.post("/", response_model=JournalEntryRead)
def create_entry(entry_in: JournalEntryCreate, db: Session = Depends(get_db)):
    try:
        entry = create_journal_entry(db, entry_in)
        return entry
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# --------------------------------------------------------
# Update an existing journal entry
# --------------------------------------------------------
@router.put("/{entry_id}", response_model=JournalEntryRead)
def update_entry(entry_id: int, entry_in: JournalEntryUpdate, db: Session = Depends(get_db)):
    try:
        entry = update_journal_entry(db, entry_id, entry_in)
        return entry
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/journal-entry/{entry_id}/post", response_model=PostJournalEntryResponse)
def api_post_journal_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = post_journal_entry(db, entry_id)
    return {"message": f"Journal entry {entry.entry_number} posted successfully", "entry": entry}

# --------------------------------------------------------
# Delete (soft delete) a draft journal entry
# --------------------------------------------------------
@router.delete("/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    if entry.status != "draft":
        raise HTTPException(status_code=400, detail="Only draft entries can be deleted")

    db.delete(entry)
    db.commit()
    return {"message": f"Journal entry {entry.entry_number} deleted successfully"}

# --------------------------------------------------------
# List journal entries
# --------------------------------------------------------
@router.get("/", response_model=list[JournalEntryRead])
def list_entries(db: Session = Depends(get_db)):
    return db.query(JournalEntry).all()
