from pydantic import BaseModel
from typing import Optional

class InventoryBase(BaseModel):
    item_id: int
    warehouse_id: int
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

    class Config:
        orm_mode = True
