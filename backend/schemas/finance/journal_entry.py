# backend/schemas/journal.py
from pydantic import BaseModel, condecimal, Field
from typing import List, Optional
from datetime import date

Decimal = condecimal(max_digits=18, decimal_places=2)

class JournalLineCreate(BaseModel):
    account_id: int
    description: Optional[str] = None
    debit: Decimal = Field(default=0) # type: ignore
    credit: Decimal = Field(default=0) # pyright: ignore[reportInvalidTypeForm]

class JournalEntryCreate(BaseModel):
    batch_id: Optional[int] = None  # optional: attach to existing batch/event
    entry_date: Optional[date] = None
    description: Optional[str] = None
    lines: List[JournalLineCreate]

class JournalLineRead(JournalLineCreate):
    id: int
    entry_id: int

    class Config:
        orm_mode = True



class JournalEntryRead(BaseModel):
    id: int
    batch_id: Optional[int]
    entry_number: str
    entry_date: date
    description: Optional[str]
    total_debit: Decimal # type: ignore
    total_credit: Decimal # type: ignore
    status: str
    lines: List[JournalLineRead] = []

    class Config:
        orm_mode = True
