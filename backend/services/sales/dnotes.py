from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.Sales.dnotes import DeliveryNote, DeliveryNoteLine
from backend.schemas.sales.dnotes import DeliveryNoteCreate


def create_delivery_note(db: Session, delivery_data: DeliveryNoteCreate):
    dn = DeliveryNote(
        sales_order_id=delivery_data.sales_order_id,
        delivery_date=delivery_data.delivery_date,
        reference=delivery_data.reference,
        status="DRAFT"
    )
    db.add(dn)
    db.flush()  # Get ID for lines

    for line in delivery_data.lines:
        dn_line = DeliveryNoteLine(
            delivery_note_id=dn.id,
            order_line_id=line.order_line_id,
            item_id=line.item_id,
            qty_shipped=line.qty_shipped,
            warehouse_id=line.warehouse_id
        )
        db.add(dn_line)

    db.commit()
    db.refresh(dn)
    return dn


def get_delivery_notes(db: Session, skip: int = 0, limit: int = 50):
    return db.query(DeliveryNote).offset(skip).limit(limit).all()


def get_delivery_note(db: Session, dn_id: int):
    dn = db.query(DeliveryNote).filter(DeliveryNote.id == dn_id).first()
    if not dn:
        raise HTTPException(status_code=404, detail="Delivery Note not found")
    return dn


def update_delivery_note_status(db: Session, dn_id: int, status: str):
    dn = get_delivery_note(db, dn_id)
    if dn.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Cannot update a cancelled Delivery Note")
    dn.status = status
    db.commit()
    db.refresh(dn)
    return dn


def delete_delivery_note(db: Session, dn_id: int):
    dn = get_delivery_note(db, dn_id)
    db.delete(dn)
    db.commit()
    return {"detail": "Delivery Note deleted"}
