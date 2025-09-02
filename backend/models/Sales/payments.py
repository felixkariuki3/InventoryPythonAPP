from sqlalchemy import (
    Column, Integer, Numeric, String, Float, DateTime, ForeignKey, Text, func
)
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


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
