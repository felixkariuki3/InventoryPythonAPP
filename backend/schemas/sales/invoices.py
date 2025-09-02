from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Invoices
# ---------------------------
class SalesInvoiceCreate(BaseModel):
    id: int
    customer_id: int
    invoice_date: datetime
    status: str
    total: Decimal
    balance: Decimal
    

class SalesInvoiceLineCreate(BaseModel):
    id: int
    item_id: str
    qty: Decimal
    unit_price: Decimal
    tax_rate: Optional[Decimal] = 0
    discount_rate: Optional[Decimal] = 0

class SalesInvoiceLineRead(BaseModel):
    id: int
    item_id: str
    qty: Decimal
    unit_price: Decimal
    tax_rate: Optional[Decimal] = 0
    discount_rate: Optional[Decimal] = 0

    class Config:
        orm_mode = True


class SalesInvoiceRead(BaseModel):
    id: int
    customer_id: int
    invoice_date: datetime
    status: str
    total: Decimal
    balance: Decimal
    lines: List[SalesInvoiceLineRead] = []

    class Config:
        orm_mode = True

class SalesInvoiceUpdate(BaseModel):
    invoice_date: datetime
    status: str
