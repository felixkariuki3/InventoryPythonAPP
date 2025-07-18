from pydantic import BaseModel

class WarehouseBase(BaseModel):
    code: str
    name: str

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    id: int

    class Config:
        orm_mode = True