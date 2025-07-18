from pydantic import BaseModel
from typing import Optional

class BOMBase(BaseModel):
    parent_item_id: int
    component_item_id: int
    quantity: int

class BOMCreate(BOMBase):
    pass

class BOMOut(BOMBase):
    id: int

    class Config:
        from_attributes = True