from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


# ---------------------------
# Sales Order + Lines
# ---------------------------
class SalesOrderLineBase(BaseModel):
    item_id: int
    ordered_qty: Decimal
    unit_price: Decimal
    tax_rate: Optional[Decimal] = 0
    discount_rate: Optional[Decimal] = 0
    warehouse_id: Optional[int] = None


class SalesOrderLineCreate(SalesOrderLineBase):
    pass


class SalesOrderLineRead(SalesOrderLineBase):
    id: int
    shipped_qty: Decimal

    class Config:
        orm_mode = True


class SalesOrderCreate(BaseModel):
    customer_id: int
    remarks: Optional[str] = None
    lines: List[SalesOrderLineCreate]


class SalesOrderRead(BaseModel):
    id: int
    customer_id: int
    order_date: datetime
    status: str
    remarks: Optional[str]
    lines: List[SalesOrderLineRead]

    class Config:
        orm_mode = True


# ---------------------------
# Delivery Notes
# ---------------------------
class DeliveryNoteLineRead(BaseModel):
    id: int
    item_id: str
    qty_shipped: Decimal

    class Config:
        orm_mode = True


class DeliveryNoteRead(BaseModel):
    id: int
    sales_order_id: int
    delivery_date: datetime
    status: str
    reference: Optional[str]
    lines: List[DeliveryNoteLineRead] = []

    class Config:
        orm_mode = True


# ---------------------------
# Invoices
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
# Payments + Allocations
# ---------------------------
class PaymentAllocationRead(BaseModel):
    id: int
    invoice_id: int
    amount_applied: Decimal

    class Config:
        orm_mode = True


class PaymentRead(BaseModel):
    id: int
    customer_id: int
    payment_date: datetime
    method: str
    reference: Optional[str]
    amount: Decimal
    unallocated_amount: Decimal
    allocations: List[PaymentAllocationRead] = []

    class Config:
        orm_mode = True


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


# ---------------------------
# Adjustments
# ---------------------------
class SalesAdjustmentRead(BaseModel):
    id: int
    customer_id: int
    invoice_id: Optional[int]
    adj_type: str
    amount: Decimal
    reason: Optional[str]
    adj_date: datetime

    class Config:
        orm_mode = True


# ---------------------------
# Stock Reservations
# ---------------------------
class StockReservationRead(BaseModel):
    id: int
    sales_order_line_id: int
    item_id: int
    warehouse_id: int
    reserved_qty: Decimal
    released_qty: Decimal
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


# ---------------------------
# Accounting Events
# ---------------------------
class AccountingEventRead(BaseModel):
    id: int
    event_type: str
    reference_id: int
    reference_table: str
    amount: Decimal
    debit_account: Optional[str]
    credit_account: Optional[str]
    currency: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
