from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Credit Notes
# ---------------------------
class CreditNoteLineRead(BaseModel):
    id: int
    item_id: str
    qty: Decimal
    unit_price: Decimal
    reason: Optional[str]

    class Config:
        orm_mode = True


class CreditNoteRead(BaseModel):
    id: int
    customer_id: int
    credit_date: datetime
    status: str
    total: Decimal
    reference_invoice_id: Optional[int]
    lines: List[CreditNoteLineRead] = []

    class Config:
        orm_mode = True
