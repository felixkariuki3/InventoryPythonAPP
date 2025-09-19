from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import date

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("journal_batches.id"), nullable=False)
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
    entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("chart_of_accounts.id"), nullable=False)
    description = Column(String, nullable=True)
    debit = Column(Numeric(18, 2), default=0)
    credit = Column(Numeric(18, 2), default=0)

    # relationships
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("ChartOfAccount")
