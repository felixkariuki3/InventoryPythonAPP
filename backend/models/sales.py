# backend/models/sales.py
from sqlalchemy import (
    Column, Integer, Numeric, String, Float, DateTime, ForeignKey, Text, func
)
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

# ---------------------------
# Customers
# ---------------------------
class SalesOrderStatus(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    PARTIALLY_SHIPPED = "PARTIALLY_SHIPPED"
    SHIPPED = "SHIPPED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    email = Column(String)
    phone = Column(String)
    terms = Column(String)
    credit_limit = Column(Float, default=0)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    sales_orders = relationship("SalesOrder", back_populates="customer")
    invoices = relationship("SalesInvoice", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")
    credit_notes = relationship("CreditNote", back_populates="customer")

# ---------------------------
# Sales Orders
# ---------------------------
class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", name="fk_sales_orders_customer_id"), nullable=False, index=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="DRAFT", index=True)
    remarks = Column(Text)

    customer = relationship("Customer", back_populates="sales_orders")
    lines = relationship("SalesOrderLine", back_populates="order", cascade="all, delete-orphan")
    delivery_notes = relationship("DeliveryNote", back_populates="sales_order")

class SalesOrderLine(Base):
    __tablename__ = "sales_order_lines"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id", name="fk_sol_order_id"), nullable=False, index=True)
    item_id = Column(String, ForeignKey("items.item_id", name="fk_sol_item_id"), nullable=False, index=True)  # TEXT
    ordered_qty = Column(Float, nullable=False)
    shipped_qty = Column(Float, default=0, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0)
    discount_rate = Column(Float, default=0)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", name="fk_sol_warehouse_id"))

    order = relationship("SalesOrder", back_populates="lines")
    item = relationship("Item", back_populates="sales_order_lines", uselist=False)
    warehouse = relationship("Warehouse")
    reservations = relationship("StockReservation", back_populates="order_line", cascade="all, delete-orphan")


# ---------------------------
# Delivery Notes (Shipments)
# ---------------------------
class DeliveryNote(Base):
    __tablename__ = "delivery_notes"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id", name="fk_dn_sales_order_id"))
    delivery_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="DRAFT", index=True)
    reference = Column(String)

    sales_order = relationship("SalesOrder", back_populates="delivery_notes")
    lines = relationship("DeliveryNoteLine", back_populates="delivery_note", cascade="all, delete-orphan")

class DeliveryNoteLine(Base):
    __tablename__ = "delivery_note_lines"

    id = Column(Integer, primary_key=True, index=True)
    delivery_note_id = Column(Integer, ForeignKey("delivery_notes.id", name="fk_dnl_delivery_note_id"), nullable=False, index=True)
    order_line_id = Column(Integer, ForeignKey("sales_order_lines.id", name="fk_dnl_order_line_id"))
    item_id = Column(String, ForeignKey("items.item_id", name="fk_dnl_item_id"), nullable=False, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", name="fk_dnl_warehouse_id"))
    qty_shipped = Column(Float, nullable=False)
    unit_cost = Column(Float)

    delivery_note = relationship("DeliveryNote", back_populates="lines")
    order_line = relationship("SalesOrderLine")
    warehouse = relationship("Warehouse")

    # item relationship optional (if you want it): relationship("Item")

# ---------------------------
# Sales Invoices
# ---------------------------
class SalesInvoice(Base):
    __tablename__ = "sales_invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", name="fk_si_customer_id"), nullable=False, index=True)
    invoice_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="DRAFT", index=True)     # DRAFT, POSTED, PARTIALLY_PAID, PAID, CANCELLED
    invoice_type = Column(String, default="CREDIT")          # CREDIT, CASH
    subtotal = Column(Float, default=0, nullable=False)
    tax_total = Column(Float, default=0, nullable=False)
    total = Column(Float, default=0, nullable=False)
    balance = Column(Float, default=0, nullable=False)
    notes = Column(Text)

    customer = relationship("Customer", back_populates="invoices")
    lines = relationship("SalesInvoiceLine", back_populates="invoice", cascade="all, delete-orphan")
    allocations = relationship("PaymentAllocation", back_populates="invoice", cascade="all, delete-orphan")

class SalesInvoiceLine(Base):
    __tablename__ = "sales_invoice_lines"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("sales_invoices.id", name="fk_sil_invoice_id"), nullable=False, index=True)
    item_id = Column(String, ForeignKey("items.item_id", name="fk_sil_item_id"), nullable=False, index=True)
    qty = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    unit_cost = Column(Float)
    tax_rate = Column(Float, default=0)
    discount_rate = Column(Float, default=0)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", name="fk_sil_warehouse_id"))
    so_line_id = Column(Integer, ForeignKey("sales_order_lines.id", name="fk_sil_so_line_id"))
    
    
    warehouse = relationship("Warehouse")
    invoice = relationship("SalesInvoice", back_populates="lines")
    # item relationship optional
    so_line = relationship("SalesOrderLine")

# ---------------------------
# Credit Notes
# ---------------------------
class CreditNote(Base):
    __tablename__ = "credit_notes"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", name="fk_cn_customer_id"), nullable=False, index=True)
    credit_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="DRAFT", index=True)     # DRAFT, POSTED, APPLIED, CANCELLED
    reference_invoice_id = Column(Integer, ForeignKey("sales_invoices.id", name="fk_cn_reference_invoice_id"))
    subtotal = Column(Float, default=0, nullable=False)
    tax_total = Column(Float, default=0, nullable=False)
    total = Column(Float, default=0, nullable=False)
    notes = Column(Text)

    customer = relationship("Customer")
    reference_invoice = relationship("SalesInvoice")
    lines = relationship("CreditNoteLine", back_populates="credit_note", cascade="all, delete-orphan")

class CreditNoteLine(Base):
    __tablename__ = "credit_note_lines"

    id = Column(Integer, primary_key=True, index=True)
    credit_note_id = Column(Integer, ForeignKey("credit_notes.id", name="fk_cnl_credit_note_id"), nullable=False, index=True)
    item_id = Column(String, ForeignKey("items.item_id", name="fk_cnl_item_id"), nullable=False, index=True)
    qty = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0)
    reason = Column(String)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", name="fk_cnl_warehouse_id"))
    
    credit_note = relationship("CreditNote", back_populates="lines")
    warehouse = relationship("Warehouse")



# ---------------------------
# Adjustments
# ---------------------------
class SalesAdjustment(Base):
    __tablename__ = "sales_adjustments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", name="fk_sadj_customer_id"), nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey("sales_invoices.id", name="fk_sadj_invoice_id"), index=True)
    adj_type = Column(String, nullable=False)   # DISCOUNT, WRITE_OFF, OTHER
    amount = Column(Float, nullable=False)
    reason = Column(Text)
    adj_date = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="adjustments")
    invoice = relationship("SalesInvoice", back_populates="adjustments")

# ---------------------------
# Payments & Allocations
# ---------------------------
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", name="fk_pay_customer_id"), nullable=False, index=True)
    payment_date = Column(DateTime, default=datetime.utcnow)
    method = Column(String, nullable=False)    # CASH, BANK, MPESA, CHEQUE, OTHER
    reference = Column(String)
    amount = Column(Float, nullable=False)
    unallocated_amount = Column(Float, default=0)
    notes = Column(Text)

    customer = relationship("Customer", back_populates="payments")
    allocations = relationship("PaymentAllocation", back_populates="payment", cascade="all, delete-orphan")

class PaymentAllocation(Base):
    __tablename__ = "payment_allocations"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id", name="fk_palloc_payment_id"), nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey("sales_invoices.id", name="fk_palloc_invoice_id"), nullable=False, index=True)
    amount_applied = Column(Float, nullable=False)

    payment = relationship("Payment", back_populates="allocations")
    invoice = relationship("SalesInvoice", back_populates="allocations")

class StockReservation(Base):
    __tablename__ = "stock_reservations"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_line_id = Column(Integer, ForeignKey("sales_order_lines.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    reserved_qty = Column(Float, nullable=False)
    released_qty = Column(Float, default=0)
    status = Column(String, default="active")  # active, fulfilled, cancelled
    created_at = Column(DateTime, default=func.now())

    # relations
    order_line = relationship("SalesOrderLine", back_populates="reservations")
    item = relationship("Item")
    warehouse = relationship("Warehouse")
    order_line = relationship("SalesOrderLine", back_populates="reservations")

class AccountingEvent(Base):
    __tablename__ = "accounting_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)  # e.g. SO_CONFIRM, INVOICE, PAYMENT, RETURN
    reference_id = Column(Integer, nullable=False)  # points to SO, invoice, payment etc.
    reference_table = Column(String, nullable=False)  # "sales_orders", "sales_invoices", etc.
    amount = Column(Float, nullable=False, default=0)
    debit_account = Column(String)
    credit_account = Column(String)
    currency = Column(String, default="KES")
    status = Column(String, default="PENDING")  # to be picked by accounting processor
    created_at = Column(DateTime, default=datetime.utcnow)

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, index=True)
    description = Column(String, nullable=True)
    entry_date = Column(DateTime, default=datetime.utcnow)

    lines = relationship("JournalLine", back_populates="journal")


class JournalLine(Base):
    __tablename__ = "journal_lines"

    id = Column(Integer, primary_key=True, index=True)
    journal_id = Column(Integer, ForeignKey("journal_entries.id"))
    account = Column(String, index=True)
    debit = Column(Numeric(12, 2), default=0)
    credit = Column(Numeric(12, 2), default=0)

    journal = relationship("JournalEntry", back_populates="lines")
# ---------------------------
# Sales Returns
# ---------------------------
class SalesReturn(Base):
    __tablename__ = "sales_returns"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"))
    sales_order_line_id = Column(Integer, ForeignKey("sales_order_lines.id"), nullable=True)
    item_id = Column(Integer, ForeignKey("items.item_id"))
    quantity = Column(Float, nullable=False)
    reason = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, approved, rejected, completed
    created_at = Column(DateTime, default=datetime.utcnow)

