from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class AccountType(str, enum.Enum):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EQUITY = "Equity"
    REVENUE = "Revenue"
    EXPENSE = "Expense"


class ReportingStatement(str, enum.Enum):
    BALANCE_SHEET = "Balance Sheet"
    INCOME_STATEMENT = "Income Statement"
    CASH_FLOW = "Cash Flow"


class ReportingGroup(Base):
    __tablename__ = "reporting_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    statement = Column(Enum(ReportingStatement), nullable=False)
    order = Column(Integer, nullable=False, default=0)

    accounts = relationship("Account", back_populates="reporting_group")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(AccountType), nullable=False)
    parent_account_id = Column(Integer, ForeignKey("accounts.id", name="fk_accounts_parent_account_id"), nullable=True)
    reporting_group_id = Column(Integer, ForeignKey("reporting_groups.id", name="fk_accounts_reporting_group_id"), nullable=True)
    is_control_account = Column(Boolean, default=False)
    currency = Column(String, default="KES")  # or USD, multi-currency support
    is_active = Column(Boolean, default=True)
    level = Column(Integer, default=1)

    parent = relationship("Account", remote_side=[id], backref="children")
    reporting_group = relationship("ReportingGroup", back_populates="accounts")
    Slines = relationship ("JournalLine", back_populates="account")


class DimensionType(str, enum.Enum):
    DEPARTMENT = "Department"
    LOCATION = "Location"
    PROJECT = "Project"
    CUSTOM = "Custom"


class Dimension(Base):
    __tablename__ = "dimensions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(DimensionType), nullable=False)
    is_active = Column(Boolean, default=True)
