from pydantic import BaseModel

class UOMCreate(BaseModel):
    name: str
    symbol: str

class UOMConversionCreate(BaseModel):
    base_uom_id: int
    target_uom: str
    factor: float

class UOMOut(BaseModel):
    id: int
    name: str
    symbol: str

    class Config:
        from_attributes = True

class UOMConversionOut(BaseModel):
    id: int
    base_uom_id: int
    target_uom: str
    factor: float

    class Config:
        from_attributes = True
