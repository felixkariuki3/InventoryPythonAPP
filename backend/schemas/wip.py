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
