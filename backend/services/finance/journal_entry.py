from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.finance.journal_entry import JournalEntry,JournalLine
from backend.schemas.finance.journal_entry import JournalEntryCreate,JournalLineCreate,JournalEntryUpdate

def create_journal_entry(db: Session, entry_in: JournalEntryCreate):
    # calculate totals
    total_debit = sum([line.debit for line in entry_in.lines])
    total_credit = sum([line.credit for line in entry_in.lines])

    if total_debit != total_credit:
        raise HTTPException(
            status_code=400,
            detail=f"Unbalanced entry: Debit {total_debit} != Credit {total_credit}"
        )

    # create entry
    db_entry = JournalEntry(
        batch_id=entry_in.batch_id,
        entry_number=entry_in.entry_number,
        entry_date=entry_in.entry_date,
        description=entry_in.description,
        total_debit=total_debit,
        total_credit=total_credit,
        status="draft"
    )

    db.add(db_entry)
    db.flush()  # get ID for linking lines

    # create lines
    for line in entry_in.lines:
        db_line = JournalLine(
            entry_id=db_entry.id,
            account_id=line.account_id,
            description=line.description,
            debit=line.debit,
            credit=line.credit
        )
        db.add(db_line)

    db.commit()
    db.refresh(db_entry)
    return db_entry


def update_journal_entry(db: Session, entry_id: int, entry_in: JournalEntryUpdate):
    db_entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")

    if entry_in.description is not None:
        db_entry.description = entry_in.description
    if entry_in.status is not None:
        db_entry.status = entry_in.status

    if entry_in.lines is not None:
        # delete old lines
        db.query(JournalLine).filter(JournalLine.entry_id == db_entry.id).delete()

        # recalc totals
        total_debit = sum([line.debit for line in entry_in.lines])
        total_credit = sum([line.credit for line in entry_in.lines])

        if total_debit != total_credit:
            raise HTTPException(
                status_code=400,
                detail=f"Unbalanced entry: Debit {total_debit} != Credit {total_credit}"
            )

        db_entry.total_debit = total_debit
        db_entry.total_credit = total_credit

        for line in entry_in.lines:
            db_line = JournalLine(
                entry_id=db_entry.id,
                account_id=line.account_id,
                description=line.description,
                debit=line.debit,
                credit=line.credit
            )
            db.add(db_line)

    db.commit()
    db.refresh(db_entry)
    return db_entry
