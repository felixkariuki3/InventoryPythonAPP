
from sqlalchemy import (
    Column, Integer, Numeric, String, Float, DateTime, ForeignKey, Text, func
)
from enum import Enum as PyEnum
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

# ---------------------------
# Sales Invoices
# ---------------------------
class InvoiceStatus(PyEnum):
    OPEN = "OPEN"
    PARTIAL = "PARTIAL"
    PAID = "PAID"

class SalesInvoice(Base):
    __tablename__ = "sales_invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", name="fk_si_customer_id"), nullable=False, index=True)
    order_id = Column(Integer,ForeignKey("sales_orders.id",name ="fk_sales_orders_order_id"),index=True)
    invoice_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(InvoiceStatus,name="invoice_status"), default=InvoiceStatus.OPEN, nullable=False)
    invoice_type = Column(String, default="CREDIT")          # CREDIT, CASH
    subtotal = Column(Float, default=0, nullable=False)
    tax_total = Column(Float, default=0, nullable=False)
    total = Column(Float, default=0, nullable=False)
    balance = Column(Float, default=0, nullable=False)
    notes = Column(Text)

    customer = relationship("Customer", back_populates="invoices")
    lines = relationship("SalesInvoiceLine", back_populates="invoice", cascade="all, delete-orphan")
    allocations = relationship("PaymentAllocation", back_populates="invoice", cascade="all, delete-orphan")
    adjustments = relationship ("SalesAdjustment", back_populates="invoice")
    order = relationship ("SalesOrder", back_populates ="invoice")

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
