from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Adjustments
# ---------------------------
class SalesAdjustmentBase(BaseModel):
    customer_id: int
    invoice_id: Optional[int] = None
    adj_type: str
    amount: Decimal
    reason: Optional[str] = None


class SalesAdjustmentCreate(SalesAdjustmentBase):
    adj_date: Optional[datetime] = None  # defaults at service/DB level


class SalesAdjustmentUpdate(BaseModel):
    invoice_id: Optional[int] = None
    adj_type: Optional[str] = None
    amount: Optional[Decimal] = None
    reason: Optional[str] = None
    adj_date: Optional[datetime] = None


class SalesAdjustmentRead(SalesAdjustmentBase):
    id: int
    adj_date: datetime

    class Config:
        orm_mode = True
