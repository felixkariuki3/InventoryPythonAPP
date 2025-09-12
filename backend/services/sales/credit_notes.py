from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal
from backend.models.Sales.credit_notes import CreditNote, CreditNoteLine
from backend.models.item import Item
from backend.schemas.sales.credit_notes import CreditNoteCreate


def calculate_totals(lines):
    subtotal = Decimal(0)
    tax_total = Decimal(0)

    for line in lines:
        line_total = Decimal(line.qty) * Decimal(line.unit_price)
        tax = line_total * Decimal(line.tax_rate if line.tax_rate else 0) / Decimal(100)
        subtotal += line_total
        tax_total += tax

    return subtotal, tax_total, subtotal + tax_total


def create_credit_note(db: Session, credit_note_data: CreditNoteCreate):
    # Calculate totals
    subtotal, tax_total, total = calculate_totals(credit_note_data.lines)

    db_credit_note = CreditNote(
        customer_id=credit_note_data.customer_id,
        credit_date=credit_note_data.credit_date,
        reference_invoice_id=credit_note_data.reference_invoice_id,
        notes=credit_note_data.notes,
        subtotal=subtotal,
        tax_total=tax_total,
        total=total,
        status="DRAFT"
    )
    db.add(db_credit_note)
    db.flush()  # Get ID before adding lines

    for line in credit_note_data.lines:
        db_line = CreditNoteLine(
            credit_note_id=db_credit_note.id,
            item_id=line.item_id,
            qty=line.qty,
            unit_price=line.unit_price,
            tax_rate=getattr(line, "tax_rate", 0),
            reason=line.reason,
            warehouse_id=line.warehouse_id
        )
        db.add(db_line)

    db.commit()
    db.refresh(db_credit_note)
    return db_credit_note


def get_credit_notes(db: Session, skip: int = 0, limit: int = 50):
    return db.query(CreditNote).offset(skip).limit(limit).all()


def get_credit_note(db: Session, credit_note_id: int):
    cn = db.query(CreditNote).filter(CreditNote.id == credit_note_id).first()
    if not cn:
        raise HTTPException(status_code=404, detail="Credit Note not found")
    return cn


def update_credit_note_status(db: Session, credit_note_id: int, status: str):
    cn = get_credit_note(db, credit_note_id)
    if cn.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Cannot update a cancelled Credit Note")

    cn.status = status
    db.commit()
    db.refresh(cn)
    return cn


def apply_credit_note(db: Session, credit_note_id: int):
    # In a real system, you’d integrate accounting here
    cn = get_credit_note(db, credit_note_id)
    if cn.status != "POSTED":
        raise HTTPException(status_code=400, detail="Credit Note must be POSTED before applying")

    cn.status = "APPLIED"
    db.commit()
    db.refresh(cn)
    return cn
