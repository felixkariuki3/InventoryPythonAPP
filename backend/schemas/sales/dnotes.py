from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


# ---------------------------
# Delivery Note Lines
# ---------------------------
class DeliveryNoteLineBase(BaseModel):
    item_id: str
    qty_shipped: Decimal
    warehouse_id: Optional[int]
    order_line_id: Optional[int]


class DeliveryNoteLineCreate(DeliveryNoteLineBase):
    pass


class DeliveryNoteLineRead(DeliveryNoteLineBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------
# Delivery Notes
# ---------------------------
class DeliveryNoteBase(BaseModel):
    sales_order_id: Optional[int]
    delivery_date: Optional[datetime]
    reference: Optional[str]


class DeliveryNoteCreate(DeliveryNoteBase):
    lines: List[DeliveryNoteLineCreate]


class DeliveryNoteRead(DeliveryNoteBase):
    id: int
    status: str
    lines: List[DeliveryNoteLineRead] = []

    class Config:
        orm_mode = True
