from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Sales Returns
# ---------------------------
class SalesReturnCreate(BaseModel):
    sales_order_id: int
    sales_order_line_id: Optional[int]
    item_id: int
    quantity: float
    reason: Optional[str] = None

class SalesReturnUpdate(BaseModel):
    status: Optional[str] = None
    quantity: Optional[float] = None  # in case adjustment is needed

class SalesReturnResponse(BaseModel):
    id: int
    sales_order_id: int
    item_id: int
    quantity: float
    status: str
    reason: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
