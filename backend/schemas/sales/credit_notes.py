from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


# ---------------------------
# Credit Note Lines
# ---------------------------
class CreditNoteLineBase(BaseModel):
    item_id: str
    qty: Decimal
    unit_price: Decimal
    reason: Optional[str]
    warehouse_id: Optional[int]


class CreditNoteLineCreate(CreditNoteLineBase):
    pass


class CreditNoteLineRead(CreditNoteLineBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------
# Credit Note
# ---------------------------
class CreditNoteBase(BaseModel):
    customer_id: int
    credit_date: Optional[datetime] = None
    reference_invoice_id: Optional[int]
    notes: Optional[str]


class CreditNoteCreate(CreditNoteBase):
    lines: List[CreditNoteLineCreate]


class CreditNoteRead(CreditNoteBase):
    id: int
    status: str
    subtotal: Decimal
    tax_total: Decimal
    total: Decimal
    lines: List[CreditNoteLineRead] = []

    class Config:
        orm_mode = True
