from typing import Optional
from pydantic import BaseModel

class UOMBase(BaseModel):
    name: str
    symbol: str

class UOMCreate(UOMBase):
    pass

class UOMOut(UOMBase):
    id: int
    class Config:
        from_attributes = True

class UOMConversionBase(BaseModel):
    item_id: Optional[int]
    base_uom_id: int
    target_uom: int
    factor: float

class UOMConversionCreate(UOMConversionBase):
    item_id: int

class UOMConversionOut(UOMConversionBase):
    id: int
    class Config:
        from_attributes = True
