from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.dependencies import get_db
from backend.services.finance.accounting_service import (
    create_accounting_event,
    post_journal_entry,
    reverse_journal_entry,
)
from backend.models.finance.accounting import JournalEntry, JournalLine, AccountingEvent
from backend.schemas.finance.accounting import (
    AccountingEventCreate,AccountingEventRead
)
from backend.schemas.finance.journal_entry import JournalEntryRead, JournalLineRead

router = APIRouter(
    prefix="/accounting",
    tags=["Accounting & Journals"],
)


# ---------------------------------------------------------------------
# 1️⃣ Create Accounting Event
# ---------------------------------------------------------------------
@router.post("/create-event", response_model=AccountingEventRead)
def create_event(payload: AccountingEventCreate, db: Session = Depends(get_db)):
    """
    Create an accounting event and corresponding journal entry + lines.
    """
    try:
        result = create_accounting_event(
            db=db,
            source_module=payload.source_module,
            reference_table=payload.reference_table,
            reference_id=payload.reference_id,
            description=payload.description,
            amount=payload.amount,
            debit_account_id=payload.debit_account_id,
            credit_account_id=payload.credit_account_id,
        )
        return {"message": "Accounting event created successfully", **result}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------------------
# 2️⃣ Post Journal Entry
# ---------------------------------------------------------------------
@router.post("/post-entry/{entry_id}", response_model=JournalEntryRead)
def post_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Post a journal entry after validating that debits = credits.
    """
    try:
        result = post_journal_entry(db, entry_id)
        return {"message": "Journal entry posted successfully", **result}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------------------
# 3️⃣ Reverse Journal Entry
# ---------------------------------------------------------------------
@router.post("/reverse-entry/{entry_id}", response_model=JournalEntryRead)
def reverse_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Reverse a posted journal entry by creating a new reversed entry.
    """
    try:
        result = reverse_journal_entry(db, entry_id)
        return {"message": "Journal entry reversed successfully", **result}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------------------
# 4️⃣ Get All Journal Entries
# ---------------------------------------------------------------------
@router.get("/entries", response_model=list[JournalEntryRead])
def list_entries(db: Session = Depends(get_db)):
    """
    Retrieve all journal entries.
    """
    return db.query(JournalEntry).all()


# ---------------------------------------------------------------------
# 5️⃣ Get Journal Lines by Entry ID
# ---------------------------------------------------------------------
@router.get("/entries/{entry_id}/lines", response_model=list[JournalLineRead])
def get_entry_lines(entry_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all journal lines belonging to a specific journal entry.
    """
    return db.query(JournalLine).filter(JournalLine.entry_id == entry_id).all()


# ---------------------------------------------------------------------
# 6️⃣ List Accounting Events
# ---------------------------------------------------------------------
@router.get("/events", response_model=list[AccountingEventRead])
def list_events(db: Session = Depends(get_db)):
    """
    Retrieve all accounting events.
    """
    return db.query(AccountingEvent).all()
