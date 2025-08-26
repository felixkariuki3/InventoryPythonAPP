# backend/routers/sales_orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.sales import (
    SalesOrderCreate, SalesOrderRead, SalesOrderUpdate,
    SalesOrderLineCreate, SalesOrderLineRead
)
from backend.services import sales_orders as sales_orders_service
from backend.database import get_db

router = APIRouter(
    prefix="/sales/orders",
    tags=["Sales Orders"]
)

# ---------------------------
# Sales Orders
# ---------------------------

@router.post("/", response_model=SalesOrderRead)
def create_sales_order(order: SalesOrderCreate, db: Session = Depends(get_db)):
    return sales_orders_service.create_sales_order(db, order)

@router.get("/{order_id}", response_model=SalesOrderRead)
def get_sales_order(order_id: int, db: Session = Depends(get_db)):
    order = sales_orders_service.get_sales_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return order

@router.get("/", response_model=list[SalesOrderRead])
def list_sales_orders(db: Session = Depends(get_db)):
    return sales_orders_service.list_sales_orders(db)

@router.put("/{order_id}", response_model=SalesOrderRead)
def update_sales_order(order_id: int, order_update: SalesOrderUpdate, db: Session = Depends(get_db)):
    return sales_orders_service.update_sales_order(db, order_id, order_update)

@router.delete("/{order_id}")
def delete_sales_order(order_id: int, db: Session = Depends(get_db)):
    return sales_orders_service.delete_sales_order(db, order_id)

# ---------------------------
# Order Processing (Flow)
# ---------------------------

@router.post("/{order_id}/reserve", response_model=SalesOrderRead)
def reserve_stock(order_id: int, db: Session = Depends(get_db)):
    return sales_orders_service.reserve_stock_for_order(db, order_id)

@router.post("/{order_id}/fulfill", response_model=SalesOrderRead)
def fulfill_order(order_id: int, db: Session = Depends(get_db)):
    return sales_orders_service.fulfill_order(db, order_id)

@router.post("/{order_id}/invoice", response_model=SalesOrderRead)
def generate_invoice(order_id: int, db: Session = Depends(get_db)):
    return sales_orders_service.generate_invoice(db, order_id)

@router.post("/{order_id}/payment")
def record_payment(order_id: int, payment_data: dict, db: Session = Depends(get_db)):
    return sales_orders_service.record_payment(db, order_id, payment_data)

@router.post("/{order_id}/adjustment")
def apply_adjustment(order_id: int, adjustment_data: dict, db: Session = Depends(get_db)):
    return sales_orders_service.apply_adjustment(db, order_id, adjustment_data)

@router.post("/{order_id}/return")
def process_return(order_id: int, return_data: dict, db: Session = Depends(get_db)):
    return sales_orders_service.process_return(db, order_id, return_data)
