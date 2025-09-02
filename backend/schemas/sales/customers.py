from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

class CustomerBase(BaseModel):
    name: str
    email: str
    phone:str
    terms:str
    credit_limit:Optional[float]
    is_active:Optional[int]

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerOut(BaseModel):
    id:int
    name:str