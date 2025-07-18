from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    item_id: int
    warehouse_id: int
    type: str
    quantity: float
    reference: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class InventoryLogOut(BaseModel):
    id: int
    item_id: int
    warehouse_id: int
    transaction_id: int
    change: float
    note: str
    timestamp: datetime

    class Config:
        from_attributes = True
