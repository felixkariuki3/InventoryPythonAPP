from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


# ---------------------------
# CREATE SCHEMAS
# ---------------------------
class SalesInvoiceLineCreate(BaseModel):
    item_id: str
    qty: Decimal
    unit_price: Decimal
    tax_rate: Optional[Decimal] = 0
    discount_rate: Optional[Decimal] = 0


class SalesInvoiceCreate(BaseModel):
    customer_id: int
    invoice_date: Optional[datetime] = None
    status: Optional[str] = "DRAFT"
    total: Decimal
    balance: Optional[Decimal] = None
    lines: List[SalesInvoiceLineCreate]


# ---------------------------
# READ SCHEMAS
# ---------------------------
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


# ---------------------------
# UPDATE SCHEMA
# ---------------------------
class SalesInvoiceUpdate(BaseModel):
    invoice_date: Optional[datetime] = None
    status: Optional[str] = None
    total: Optional[Decimal] = None
    balance: Optional[Decimal] = None
