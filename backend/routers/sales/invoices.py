from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.schemas.sales.sales_order import SalesOrderRead
from backend.services.sales import accounting

router= APIRouter(prefix="/sales/invoices",tags="Invoices")

@router.post("/{order_id}/invoice", response_model=SalesOrderRead)
def generate_invoice(order_id: int, db: Session = Depends(get_db)):
    return accounting.post_invoice(db, order_id)