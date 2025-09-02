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
