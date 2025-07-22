# backend/schemas/production.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ProductionStatus(str, Enum):
    planned = "Planned"
    in_progress = "In Progress"
    completed = "Completed"
    cancelled = "Cancelled"


class ProductionOperationCreate(BaseModel):
    name: str
    sequence: int
    duration_minutes: float


class ProductionOrderCreate(BaseModel):
    item_id: int
    quantity: float
    operations: List[ProductionOperationCreate]


class ProductionOrderResponse(BaseModel):
    id: int
    item_id: int
    quantity: float
    status: ProductionStatus
    start_date: datetime
    end_date: Optional[datetime]
    operations: List[ProductionOperationCreate]

    class Config:
        from_attributes = True
