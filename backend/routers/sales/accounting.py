from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.models.finance.accounting import JournalEntry, JournalLine
from backend.services.sales.accounting import SalesAccountingService
from backend.schemas.finance.accounting import (
    JournalEntryRead,
    JournalLineRead
)

router = APIRouter(
    prefix="/sales/accounting",
    tags=["Accounting"]
)

# ---------------------------
# Invoice Posting Endpoint
# ---------------------------
@router.post("/post-invoice/{order_id}", response_model=JournalEntryRead)
def post_invoice(order_id: int, db: Session = Depends(get_db)):
    try:
        journal = SalesAccountingService.post_invoice(db, order_id)
        return journal
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ---------------------------
# Payment Posting Endpoint
# ---------------------------
@router.post("/post-payment/{payment_id}", response_model=JournalEntryRead)
def post_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        journal = SalesAccountingService.post_payment(db, payment_id)
        return journal
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ---------------------------
# Get Journal Entry by ID
# ---------------------------
@router.get("/journal/{journal_id}", response_model=JournalEntryRead)
def get_journal_entry(journal_id: int, db: Session = Depends(get_db)):
    journal = db.query(JournalEntry).filter(JournalEntry.id == journal_id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return journal


# ---------------------------
# List Journal Entries
# ---------------------------
@router.get("/journals", response_model=List[JournalEntryRead])
def list_journals(db: Session = Depends(get_db)):
    return db.query(JournalEntry).all()


# ---------------------------
# List Journal Lines for a Journal
# ---------------------------
@router.get("/journal/{journal_id}/lines", response_model=List[JournalLineRead])
def list_journal_lines(journal_id: int, db: Session = Depends(get_db)):
    lines = db.query(JournalLine).filter(JournalLine.journal_id == journal_id).all()
    if not lines:
        raise HTTPException(status_code=404, detail="No journal lines found")
    return lines
