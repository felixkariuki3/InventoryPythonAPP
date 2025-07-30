# backend/schemas/purchase.py
from pydantic import BaseModel
from typing import List
from datetime import datetime

class PurchaseOrderLineCreate(BaseModel):
    item_id: int
    quantity: float
    unit_cost: float

class PurchaseOrderCreate(BaseModel):
    supplier_name: str
    lines: List[PurchaseOrderLineCreate]

class PurchaseOrderLineOut(PurchaseOrderLineCreate):
    id: int

class PurchaseOrderOut(BaseModel):
    id: int
    supplier_name: str
    order_date: datetime
    status: str
    lines: List[PurchaseOrderLineOut]

    class Config:
        from_attributes = True
