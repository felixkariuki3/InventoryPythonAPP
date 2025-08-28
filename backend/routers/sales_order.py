# backend/routers/sales_orders.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.sales import (
    PaymentCreate, PaymentRead, PaymentUpdate, ReservationCreate, 
    ReservationRead, ReservationUpdate, SalesOrderCreate, SalesOrderRead, 
    SalesOrderUpdate,SalesReturnCreate,SalesReturnResponse,SalesReturnUpdate,
    SalesOrderLineCreate, SalesOrderLineRead,SalesAdjustmentBase,SalesAdjustmentCreate,
    SalesAdjustmentRead,SalesAdjustmentUpdate
)
from backend.services.sales import returns,accounting,payments,sales_order,reservations,adjustments
from backend.crud.sales_order import delete_sales_order
from backend.dependencies import get_db

router = APIRouter(
    prefix="/sales/orders",
    tags=["Sales Orders"]
)

# ---------------------------
# Sales Orders
# ---------------------------

@router.post("/", response_model=SalesOrderRead)
def create_sales_order(order: SalesOrderCreate, db: Session = Depends(get_db)):
    return sales_order.create_sales_order(db, order)

@router.get("/{order_id}", response_model=SalesOrderRead)
def get_sales_order(order_id: int, db: Session = Depends(get_db)):
    order = sales_order.get_sales_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return order

@router.get("/", response_model=list[SalesOrderRead])
def list_sales_orders(db: Session = Depends(get_db)):
    return sales_order.list_sales_orders(db)

@router.put("/{order_id}", response_model=SalesOrderRead)
def update_sales_order(order_id: int, order_update: SalesOrderUpdate, db: Session = Depends(get_db)):
    return sales_order.update_sales_order(db, order_id, order_update)

@router.delete("/{order_id}")
def delete_sales_order(order_id: int, db: Session = Depends(get_db)):
    return delete_sales_order(db, order_id)

# ---------------------------
# Order Processing (Flow)
# ---------------------------

@router.post("/", response_model=ReservationRead)
def create_reservation(reservation_in: ReservationCreate, db: Session = Depends(get_db)):
    return reservations.ReservationService.create_reservation(db, reservation_in)

@router.put("/{reservation_id}", response_model=ReservationRead)
def update_reservation(reservation_id: int, reservation_in: ReservationUpdate, db: Session = Depends(get_db)):
    return reservations.ReservationService.update_reservation(db, reservation_id, reservation_in)

@router.post("/{reservation_id}/release", response_model=ReservationRead)
def release_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return reservations.ReservationService.release_reservation(db, reservation_id)

@router.get("/", response_model=List[ReservationRead])
def list_reservations(order_line_id: int = None, db: Session = Depends(get_db)):
    return reservations.ReservationService.list_reservations(db, order_line_id)

@router.post("/{order_id}/fulfill", response_model=SalesOrderRead)
def fulfill_order(order_id: int, db: Session = Depends(get_db)):
    return sales_order.fulfill_order(db, order_id)

@router.post("/{order_id}/invoice", response_model=SalesOrderRead)
def generate_invoice(order_id: int, db: Session = Depends(get_db)):
    return accounting.post_invoice(db, order_id)

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


@router.post("/", response_model=SalesAdjustmentRead)
def create(adjustment: SalesAdjustmentCreate, db: Session = Depends(get_db)):
    return adjustments.create_adjustment(db, adjustment)

@router.get("/{adj_id}", response_model=SalesAdjustmentRead)
def get(adj_id: int, db: Session = Depends(get_db)):
    adj = adjustments.get_adjustment(db, adj_id)
    if not adj:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    return adj

@router.get("/", response_model=List[SalesAdjustmentRead])
def list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return adjustments.get_adjustments(db, skip, limit)

@router.put("/{adj_id}", response_model=SalesAdjustmentRead)
def update(adj_id: int, adjustment: SalesAdjustmentUpdate, db: Session = Depends(get_db)):
    adj = adjustments.update_adjustment(db, adj_id, adjustment)
    if not adj:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    return adj

@router.delete("/{adj_id}", response_model=SalesAdjustmentRead)
def delete(adj_id: int, db: Session = Depends(get_db)):
    adj = adjustments.delete_adjustment(db, adj_id)
    if not adj:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    return adj

@router.post("/", response_model=SalesReturnResponse)
def create_sales_return(return_data: SalesReturnCreate, db: Session = Depends(get_db)):
    return returns.create_return(db, return_data)

@router.put("/{return_id}", response_model=SalesReturnResponse)
def update_sales_return(return_id: int, return_data: SalesReturnUpdate, db: Session = Depends(get_db)):
    updated = returns.update_return(db, return_id, return_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Return not found")
    return updated

@router.post("/{return_id}/process", response_model=SalesReturnResponse)
def process_sales_return(return_id: int, db: Session = Depends(get_db)):
    processed = returns.process_return(db, return_id)
    if not processed:
        raise HTTPException(status_code=400, detail="Return cannot be processed")
    return processed