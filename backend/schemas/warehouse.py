from pydantic import BaseModel
from typing import Optional

class WarehouseBase(BaseModel):
    name: Optional [str] = None
    location: str

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    id: int

    class Config:
        orm_mode = True