from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
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

class SalesOrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    order_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    # optionally allow line updates
    lines: Optional[List[SalesOrderLineCreate]] = None

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
class SalesAdjustmentBase(BaseModel):
    customer_id: int
    invoice_id: Optional[int] = None
    adj_type: str
    amount: Decimal
    reason: Optional[str] = None


class SalesAdjustmentCreate(SalesAdjustmentBase):
    adj_date: Optional[datetime] = None  # defaults at service/DB level


class SalesAdjustmentUpdate(BaseModel):
    invoice_id: Optional[int] = None
    adj_type: Optional[str] = None
    amount: Optional[Decimal] = None
    reason: Optional[str] = None
    adj_date: Optional[datetime] = None


class SalesAdjustmentRead(SalesAdjustmentBase):
    id: int
    adj_date: datetime

    class Config:
        orm_mode = True

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
# ---------------------------
# Sales Returns
# ---------------------------
class SalesReturnCreate(BaseModel):
    sales_order_id: int
    sales_order_line_id: Optional[int]
    item_id: int
    quantity: float
    reason: Optional[str] = None

class SalesReturnUpdate(BaseModel):
    status: Optional[str] = None
    quantity: Optional[float] = None  # in case adjustment is needed

class SalesReturnResponse(BaseModel):
    id: int
    sales_order_id: int
    item_id: int
    quantity: float
    status: str
    reason: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
