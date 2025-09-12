from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.dependencies import get_db
from backend.schemas.sales.dnotes import DeliveryNoteCreate, DeliveryNoteRead
from backend.services.sales import dnotes as service

router = APIRouter(prefix="/sales/delivery-notes", tags=["Delivery Notes"])


@router.post("/", response_model=DeliveryNoteRead)
def create_delivery(delivery_note: DeliveryNoteCreate, db: Session = Depends(get_db)):
    return service.create_delivery_note(db, delivery_note)


@router.get("/", response_model=List[DeliveryNoteRead])
def list_deliveries(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return service.get_delivery_notes(db, skip=skip, limit=limit)


@router.get("/{dn_id}", response_model=DeliveryNoteRead)
def get_delivery(dn_id: int, db: Session = Depends(get_db)):
    return service.get_delivery_note(db, dn_id)


@router.put("/{dn_id}/status", response_model=DeliveryNoteRead)
def update_delivery_status(dn_id: int, status: str, db: Session = Depends(get_db)):
    return service.update_delivery_note_status(db, dn_id, status)


@router.delete("/{dn_id}")
def delete_delivery(dn_id: int, db: Session = Depends(get_db)):
    return service.delete_delivery_note(db, dn_id)
