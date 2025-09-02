from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Delivery Notes
# ---------------------------
class DeliveryNoteLineRead(BaseModel):
    id: int
    item_id: str
    qty_shipped: Decimal

    class Config:
        orm_mode = True


class DeliveryNoteRead(BaseModel):
    id: int
    sales_order_id: int
    delivery_date: datetime
    status: str
    reference: Optional[str]
    lines: List[DeliveryNoteLineRead] = []

    class Config:
        orm_mode = True

