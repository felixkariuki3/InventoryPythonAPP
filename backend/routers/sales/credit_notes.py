from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.dependencies import get_db
from backend.schemas.sales.credit_notes import CreditNoteCreate, CreditNoteRead
from services.sales import credit_notes as service

router = APIRouter(prefix="/credit-notes", tags=["Credit Notes"])


@router.post("/", response_model=CreditNoteRead)
def create_credit_note(credit_note: CreditNoteCreate, db: Session = Depends(get_db)):
    return service.create_credit_note(db, credit_note)


@router.get("/", response_model=List[CreditNoteRead])
def list_credit_notes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return service.get_credit_notes(db, skip=skip, limit=limit)


@router.get("/{credit_note_id}", response_model=CreditNoteRead)
def get_credit_note(credit_note_id: int, db: Session = Depends(get_db)):
    return service.get_credit_note(db, credit_note_id)


@router.put("/{credit_note_id}/status", response_model=CreditNoteRead)
def update_credit_note_status(credit_note_id: int, status: str, db: Session = Depends(get_db)):
    return service.update_credit_note_status(db, credit_note_id, status)


@router.put("/{credit_note_id}/apply", response_model=CreditNoteRead)
def apply_credit_note(credit_note_id: int, db: Session = Depends(get_db)):
    return service.apply_credit_note(db, credit_note_id)
