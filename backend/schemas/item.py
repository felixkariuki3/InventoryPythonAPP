from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    item_id: int
    name: str
    description: Optional[str] = None
    quantity: int
    warehouse_id: int
    average_cost: float


class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int
    name: str
    item_id: int
    quantity: float
    average_cost: Optional[float] = None

    class Config:
        from_attributes = True  # For SQLAlchemy ORM compatibility in Pydantic v2
