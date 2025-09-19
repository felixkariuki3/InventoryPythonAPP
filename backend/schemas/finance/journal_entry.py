from pydantic import BaseModel, condecimal
from typing import List, Optional
from datetime import date

# ---------------------------
# Journal Line
# ---------------------------
class JournalLineBase(BaseModel):
    account_id: int
    description: Optional[str] = None
    debit: condecimal(max_digits=18, decimal_places=2) = 0 # type: ignore
    credit: condecimal(max_digits=18, decimal_places=2) = 0 # type: ignore

class JournalLineCreate(JournalLineBase):
    pass

class JournalLineRead(JournalLineBase):
    id: int

    class Config:
        from_attributes = True

# ---------------------------
# Journal Entry
# ---------------------------
class JournalEntryBase(BaseModel):
    batch_id: int
    entry_number: str
    entry_date: date
    description: Optional[str] = None

class JournalEntryCreate(JournalEntryBase):
    lines: List[JournalLineCreate]

class JournalEntryUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    lines: Optional[List[JournalLineCreate]] = None

class JournalEntryRead(JournalEntryBase):
    id: int
    total_debit: condecimal(max_digits=18, decimal_places=2) # type: ignore
    total_credit: condecimal(max_digits=18, decimal_places=2) # type: ignore
    status: str
    lines: List[JournalLineRead] = []

    class Config:
        from_attributes = True
