from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True