# backend/models/sales.py
import enum
from sqlalchemy import (
    Column, Integer, Numeric, String, Float, DateTime, ForeignKey, Text, func
)
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


# ---------------------------
# Sales Orders
# ---------------------------

class SalesOrderStatus(enum.Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    PARTIALLY_SHIPPED = "partially_shipped"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
    
class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", name="fk_sales_orders_customer_id"), nullable=False, index=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="DRAFT", index=True)
    remarks = Column(Text)
    due_date=Column(DateTime, default=datetime.utcnow)
    total_amount=Column(Float, default=0)

    customer = relationship("Customer", back_populates="sales_orders")
    lines = relationship("SalesOrderLine", back_populates="order", cascade="all, delete-orphan")
    delivery_notes = relationship("DeliveryNote", back_populates="sales_order")
    invoice = relationship("SalesInvoice", back_populates ="order")
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
    line_total= Column(Float, default=0)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", name="fk_sol_warehouse_id"))

    order = relationship("SalesOrder", back_populates="lines")
    item = relationship("Item", back_populates="sales_order_lines", uselist=False)
    warehouse = relationship("Warehouse")
    reservations = relationship("StockReservation", back_populates="order_line", cascade="all, delete-orphan")



