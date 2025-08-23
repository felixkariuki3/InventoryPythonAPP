# backend/routers/purchase.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models
from backend.models.purchase import PurchaseOrder, PurchaseOrderLine
from backend.schemas import purchase as schemas
from backend.crud.purchase import create_purchase_order as create_po, get_purchase_order, list_purchase_orders
from backend.services.purchase import receive_purchase_order

router = APIRouter(prefix='/purchase',tags=["purchase"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.PurchaseOrderOut)
def create_purchase_order(order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    return create_po(db, order)

@router.get("/", response_model=list[schemas.PurchaseOrderOut])
def list_purchase_orders(db: Session = Depends(get_db)):
    return db.query(PurchaseOrder).all()

@router.get("/", response_model=List[schemas.PurchaseOrderOut])
def list_orders(db: Session = Depends(get_db)):
    return list_purchase_orders(db)
#Get order by id
@router.get("/{order_id}", response_model=schemas.PurchaseOrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = get_purchase_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
#Receiving orders and marking them as received
@router.post("/{order_id}/receive")
def receive_order(order_id: int, receipt_req: schemas.ReceiptRequest, db: Session = Depends(get_db)):
    return receive_purchase_order(db, order_id, receipt_req.receipts)