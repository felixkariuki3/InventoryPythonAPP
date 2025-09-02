from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Payments + Allocations
# ---------------------------
class PaymentAllocationBase(BaseModel):
    invoice_id: int
    amount_applied: Decimal


class PaymentAllocationCreate(PaymentAllocationBase):
    pass


class PaymentAllocationRead(PaymentAllocationBase):
    id: int

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    customer_id: int
    payment_date: Optional[datetime] = None
    method: str
    reference: Optional[str]
    amount: Decimal
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    allocations: List[PaymentAllocationCreate] = []


class PaymentUpdate(BaseModel):
    payment_date: Optional[datetime]
    method: Optional[str]
    reference: Optional[str]
    amount: Optional[Decimal]
    notes: Optional[str]


class PaymentRead(PaymentBase):
    id: int
    unallocated_amount: Decimal
    allocations: List[PaymentAllocationRead] = []

    class Config:
        orm_mode = True
