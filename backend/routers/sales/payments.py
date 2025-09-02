from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.schemas.sales.payments import PaymentCreate, PaymentRead, PaymentUpdate
from backend.services.sales import payments

router = APIRouter(prefix="/sales/payments",tags=["payments"])

@router.post("/", response_model=PaymentRead)
def create_payment(payment_in: PaymentCreate, db: Session = Depends(get_db)):
    return payments.create_payment(db, payment_in)


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = payments.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/", response_model=list[PaymentRead])
def list_payments(customer_id: int = None, db: Session = Depends(get_db)):
    return payments.list_payments(db, customer_id)


@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: int, payment_in: PaymentUpdate, db: Session = Depends(get_db)):
    payment = payments.update_payment(db, payment_id, payment_in)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = payments.delete_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"detail": "Payment deleted"}