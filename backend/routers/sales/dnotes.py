from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.schemas.sales.sales_order import SalesOrderRead
from backend.services.sales import sales_order

router = APIRouter(prefix="/sales/dnotes",tags="Delivery Notes")


@router.post("/{order_id}/fulfill", response_model=SalesOrderRead)
def fulfill_order(order_id: int, db: Session = Depends(get_db)):
    return sales_order.fulfill_order(db, order_id)