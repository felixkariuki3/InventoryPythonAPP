from sqlalchemy.orm import Session
from backend.models.Sales.credit_notes import CreditNote, CreditNoteLine
from backend.schemas.sales import (
    CreditNoteCreate, CreditNoteUpdate, CreditNoteLineCreate
)

# ---- Credit Note CRUD ----
def create_credit_note(db: Session, note: CreditNoteCreate):
    db_note = CreditNote(
        customer_id=note.customer_id,
        invoice_id=note.invoice_id,
        note_date=note.note_date,
        status=note.status or "draft",
        total_amount=0.0
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_credit_note(db: Session, note_id: int):
    return db.query(CreditNote).filter(CreditNote.id == note_id).first()


def list_credit_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CreditNote).offset(skip).limit(limit).all()


def update_credit_note(db: Session, note_id: int, note_update: CreditNoteUpdate):
    db_note = db.query(CreditNote).filter(CreditNote.id == note_id).first()
    if not db_note:
        return None
    for key, value in note_update.dict(exclude_unset=True).items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_credit_note(db: Session, note_id: int):
    db_note = db.query(CreditNote).filter(CreditNote.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note


# ---- Credit Note Line CRUD ----
def add_credit_note_line(db: Session, note_id: int, line: CreditNoteLineCreate):
    db_line = CreditNoteLine(
        note_id=note_id,
        item_id=line.item_id,
        quantity=line.quantity,
        unit_price=line.unit_price,
        line_total=line.quantity * line.unit_price
    )
    db.add(db_line)

    # Update credit note total
    note = db.query(CreditNote).filter(CreditNote.id == note_id).first()
    if note:
        note.total_amount += db_line.line_total

    db.commit()
    db.refresh(db_line)
    return db_line


def list_credit_note_lines(db: Session, note_id: int):
    return db.query(CreditNoteLine).filter(CreditNoteLine.note_id == note_id).all()
