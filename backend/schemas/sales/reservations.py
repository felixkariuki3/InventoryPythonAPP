from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Stock Reservations
# ---------------------------
class ReservationBase(BaseModel):
    order_line_id: int
    item_id: int
    reserved_qty: Decimal

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    reserved_qty: Optional[Decimal] = None
    status: Optional[str] = None

class ReservationRead(ReservationBase):
    id: int
    reserved_date: datetime
    status: str

    class Config:
        orm_mode = True
