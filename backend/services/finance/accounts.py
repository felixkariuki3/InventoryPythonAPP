from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.finance.finance import Account,AccountType
from backend.schemas.finance.finance import Account,AccountType,AccountCreate,AccountUpdate


def create_account(db: Session, account_in: AccountCreate):
    account = Account(**account_in.dict())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

def list_accounts(db: Session, skip: int = 0, limit: int = 100, active: bool = True):
    query = db.query(Account)
    if active:
        query = query.filter(Account.is_active == True)
    return query.offset(skip).limit(limit).all()

def update_account(db: Session, account_id: int, account_in: AccountUpdate):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    for field, value in account_in.dict(exclude_unset=True).items():
        setattr(account, field, value)

    db.commit()
    db.refresh(account)
    return account

def delete_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account.is_active = False  # soft delete
    db.commit()
    return account
