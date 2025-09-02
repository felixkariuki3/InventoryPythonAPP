from sqlalchemy import (
    Column, Integer, Numeric, String, Float, DateTime, ForeignKey, Text, func
)
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

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