from sqlalchemy import (
    Column, Date, Integer, Numeric, String, Float, DateTime, ForeignKey, Text, func
)
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import date, datetime
from backend.database import Base

class AccountingEvent(Base):
    __tablename__ = "accounting_events"

    id = Column(Integer, primary_key=True, index=True)
    batch_no = Column(String, unique=True, index=True, nullable=False)
    source_module = Column(String, nullable=False)  # SALES, PROCUREMENT, INVENTORY, CASHBOOK, etc.
    reference_id = Column(Integer, nullable=True)   # optional link back to SO, PO, etc.
    reference_table = Column(String, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False, default=0)
    debit_account = Column(String)
    credit_account = Column(String)
    currency = Column(String, default="KES")
    status = Column(String, default="draft")  # draft, posted, reversed
    created_at = Column(DateTime, default=datetime.utcnow)
    posted_at = Column(DateTime, nullable=True)

    entries = relationship("JournalEntry", back_populates="batch")


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    batch_no = Column(Integer, ForeignKey("accounting_events.id",name="fk_journal_entries_batch_no"), nullable=False)
    entry_number = Column(String, index=True, nullable=False)  # sequential within batch
    entry_date = Column(Date, default=date.today, nullable=False)
    description = Column(String, nullable=True)
    total_debit = Column(Numeric(18, 2), default=0)
    total_credit = Column(Numeric(18, 2), default=0)
    status = Column(String, default="draft")  # draft / posted / cancelled

    # relationships
    batch = relationship("JournalBatch", back_populates="entries")
    lines = relationship("JournalLine", back_populates="entry", cascade="all, delete-orphan")


class JournalLine(Base):
    __tablename__ = "journal_lines"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id",name="fk_journal_lines_entry_id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.code"), nullable=False)
    description = Column(String, nullable=True)
    debit = Column(Numeric(18, 2), default=0)
    credit = Column(Numeric(18, 2), default=0)

    # relationships
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account", back_populates="Slines")
