from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date
from decimal import Decimal

# ---------------------------
# Accounting Events
# ---------------------------

class AccountingEventCreate(BaseModel):
    id: int
    source_module: Optional[str]
    reference_id: int
    reference_table: str
    amount: Decimal
    debit_account: Optional[str]
    credit_account: Optional[str]
    source_module: Optional[str]
    currency: str
    description: str
    status: str
    posted_at: datetime
    created_at: datetime

class AccountingEventRead(BaseModel):
    id: int
    source_module: str
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
    status: Optional[str] = None 

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
    
