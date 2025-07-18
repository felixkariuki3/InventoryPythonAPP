from pydantic import BaseModel

class BOMBase(BaseModel):
    parent_item_id: int
    component_item_id: int
    quantity_required: int

class BOMCreate(BOMBase):
    pass

class BOM(BOMBase):
    id: int

    class Config:
        orm_mode = True
