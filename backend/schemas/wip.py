# backend/schemas/wip.py
from pydantic import BaseModel
from datetime import datetime


class WIPCreate(BaseModel):
    production_order_id: int
    issued_quantity: float = 0.0


class WIPUpdate(BaseModel):
    completed_quantity: float
    status: str


class WIPOut(BaseModel):
    id: int
    production_order_id: int
    issued_quantity: float
    completed_quantity: float
    status: str
    updated_at: datetime

    class Config:
        from_attributes = True

# schemas/wip.py

class WIPEntry(BaseModel):
    id: int
    production_order_id: int
    item_id: int
    quantity_issued: float
    cost_per_unit: float
    total_cost: float
    issued_at: datetime

    class Config:
        orm_mode = True

