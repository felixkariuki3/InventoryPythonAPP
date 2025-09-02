from sqlalchemy import (
    Column, Integer, Numeric, String, Float, DateTime, ForeignKey, Text, func
)
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

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
