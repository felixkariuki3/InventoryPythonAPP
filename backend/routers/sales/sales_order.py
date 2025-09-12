# backend/routers/sales_orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.sales.sales_order import (
    SalesOrderCreate, SalesOrderRead, 
    SalesOrderUpdate
)
from backend.services.sales.sales_order import SalesOrderService
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
    return SalesOrderService.create_order(db, order)

@router.get("/{order_id}", response_model=SalesOrderRead)
def get_sales_order(order_id: int, db: Session = Depends(get_db)):
    order = SalesOrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return order

@router.get("/", response_model=list[SalesOrderRead])
def list_sales_orders(db: Session = Depends(get_db)):
    return SalesOrderService.list_orders(db)

@router.put("/{order_id}", response_model=SalesOrderRead)
def update_sales_order(order_id: int, order_update: SalesOrderUpdate, db: Session = Depends(get_db)):
    updated = SalesOrderService.update_order(db, order_id, order_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return updated

@router.delete("/{order_id}")
def delete_sales_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    deleted = SalesOrderService.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return {"message": "Sales order deleted successfully"}
