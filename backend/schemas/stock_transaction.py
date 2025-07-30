from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Literal, Optional

class TransactionBase(BaseModel):
    item_id: int
    warehouse_id: int
    type: Literal["receipt", "issue", "adjustment", "transfer"]
    quantity: float
    reference: Optional[str] = None
    unit_cost: Optional[float] = None

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

class TransferTransaction(BaseModel):
    item_id: int
    source_warehouse_id: int
    destination_warehouse_id: int
    quantity: float
    reference: Optional[str] = None
class IssueCreate(BaseModel):
    item_id: int
    warehouse_id: int
    quantity: int
    reference: Optional[str] = None

    @field_validator("quantity")
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than zero")
        return value