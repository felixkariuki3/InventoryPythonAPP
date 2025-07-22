# backend/schemas/production_order.py

from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class OrderStatus(str, Enum):
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class ProductionOrderCreate(BaseModel):
    item_id: int
    quantity: float
    scheduled_date: Optional[datetime] = None
    note: Optional[str] = None

class ProductionOrderOut(BaseModel):
    id: int
    item_id: int
    quantity: float
    status: OrderStatus
    scheduled_date: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    note: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
