# backend/routers/sales_orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.sales.sales_order import (
    SalesOrderCreate, SalesOrderRead, 
    SalesOrderUpdate
)
from backend.services.sales import sales_order
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











