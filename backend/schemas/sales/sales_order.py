from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Sales Order + Lines
# ---------------------------
class SalesOrderLineBase(BaseModel):
    item_id: int
    ordered_qty: Decimal
    unit_price: Decimal
    tax_rate: Optional[Decimal] = 0
    discount_rate: Optional[Decimal] = 0
    warehouse_id: Optional[int] = None
    line_total: Decimal


class SalesOrderLineCreate(SalesOrderLineBase):
    pass


class SalesOrderLineRead(SalesOrderLineBase):
    id: int
    shipped_qty: Decimal

    class Config:
        orm_mode = True


class SalesOrderCreate(BaseModel):
    customer_id: int
    order_date:date
    due_date:Optional[date] = None
    remarks: Optional[str] = None
    status: Optional[str] = None
    lines: List[SalesOrderLineCreate]

class SalesOrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    order_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    # optionally allow line updates
    lines: Optional[List[SalesOrderLineCreate]] = None

class SalesOrderRead(BaseModel):
    id: int
    customer_id: int
    order_date: datetime
    status: str
    remarks: Optional[str]
    lines: List[SalesOrderLineRead]

    class Config:
        orm_mode = True

