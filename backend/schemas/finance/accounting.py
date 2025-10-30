from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Accounting Events
# ---------------------------

class AccountingEventCreate(BaseModel):
    id: int
    event_type: str
    reference_id: int
    reference_table: str
    amount: Decimal
    debit_account: Optional[str]
    credit_account: Optional[str]
    currency: str
    status: str
    created_at: datetime

class AccountingEventRead(BaseModel):
    id: int
    event_type: str
    reference_id: int
    reference_table: str
    amount: Decimal
    debit_account: Optional[str]
    credit_account: Optional[str]
    currency: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class JournalEntryCreate(BaseModel):
    id : int
    reference : str
    description : str
    entry_date : datetime

class JournalEntryRead(JournalEntryCreate):
    pass

class JournalLineCreate (BaseModel):
    id : int
    journal_id: int
    account: str
    debit: float
    credit: float

class JournalLineRead(JournalLineCreate):
    pass
    
