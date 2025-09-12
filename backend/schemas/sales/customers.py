from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Shared properties
class CustomerBase(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    terms: Optional[str]
    credit_limit: Optional[float] = 0
    is_active: Optional[int] = 1


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CustomerOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
