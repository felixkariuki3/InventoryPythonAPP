# backend/schemas/purchase.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PurchaseOrderLineCreate(BaseModel):
    item_id: int
    quantity: float
    unit_cost: float
    warehouse_id : Optional[int]

class PurchaseOrderCreate(BaseModel):
    supplier_id: str
    lines: List[PurchaseOrderLineCreate]
    order_date: Optional[datetime]= None
    status:Optional[str]

class PurchaseOrderLineOut(PurchaseOrderLineCreate):
    id: int

class PurchaseOrderOut(BaseModel):
    id: int
    supplier_id: str
    order_date: datetime
    status: str
    lines: List[PurchaseOrderLineOut]

    class Config:
        from_attributes = True

class ReceiptLine(BaseModel):
    line_id: int
    received_qty: int

class ReceiptRequest(BaseModel):
    receipts: List[ReceiptLine]
