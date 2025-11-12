from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime, date
from backend.database import Base

class JournalBatch(Base):
    __tablename__ = "journal_batches"

    id = Column(Integer, primary_key=True, index=True)
    batch_no = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    source_module = Column(String, nullable=True, default = "GENERAL LEDGER")  # e.g., SALES, INVENTORY, PAYROLL
    total_debit = Column(Numeric(18, 2), default=0)
    total_credit = Column(Numeric(18, 2), default=0)
    status = Column(String, default="draft")  # draft → approved → posted
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    posted_at = Column(DateTime, nullable=True)

    # Relationships
    entries = relationship("JournalEntry", back_populates="batch", cascade="all, delete-orphan")
