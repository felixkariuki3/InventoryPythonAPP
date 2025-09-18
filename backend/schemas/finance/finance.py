from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class AccountType(str, Enum):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EQUITY = "Equity"
    REVENUE = "Revenue"
    EXPENSE = "Expense"


class ReportingStatement(str, Enum):
    BALANCE_SHEET = "Balance Sheet"
    INCOME_STATEMENT = "Income Statement"
    CASH_FLOW = "Cash Flow"


class DimensionType(str, Enum):
    DEPARTMENT = "Department"
    LOCATION = "Location"
    PROJECT = "Project"
    CUSTOM = "Custom"


# -----------------
# Reporting Groups
# -----------------
class ReportingGroupBase(BaseModel):
    name: str
    statement: ReportingStatement
    order: int = 0


class ReportingGroupCreate(ReportingGroupBase):
    pass


class ReportingGroupOut(ReportingGroupBase):
    id: int

    class Config:
        orm_mode = True


# -----------------
# Accounts
# -----------------
class AccountBase(BaseModel):
    code: str
    name: str
    type: AccountType
    parent_account_id: Optional[int] = None
    reporting_group_id: Optional[int] = None
    is_control_account: bool = False
    currency: str = "KES"
    is_active: bool = True
    level: int = 1


class AccountCreate(AccountBase):
    pass


class AccountOut(AccountBase):
    id: int

    class Config:
        orm_mode = True


# -----------------
# Dimensions
# -----------------
class DimensionBase(BaseModel):
    name: str
    type: DimensionType
    is_active: bool = True


class DimensionCreate(DimensionBase):
    pass


class DimensionOut(DimensionBase):
    id: int

    class Config:
        orm_mode = True
