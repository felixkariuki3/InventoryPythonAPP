from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.dependencies import get_db
from backend.schemas.finance.finance import AccountCreate,AccountOut,AccountUpdate
from backend.services.finance import accounts as service

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=AccountOut)
def create_account(account_in: AccountCreate, db: Session = Depends(get_db)):
    return service.create_account(db, account_in)


@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db)):
    return service.get_account(db, account_id)


@router.get("/", response_model=List[AccountOut])
def list_accounts(skip: int = 0, limit: int = 100, active: Optional[bool] = None, db: Session = Depends(get_db)):
    return service.list_accounts(db, skip=skip, limit=limit, active=active)


@router.put("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, account_in: AccountUpdate, db: Session = Depends(get_db)):
    return service.update_account(db, account_id, account_in)


@router.delete("/{account_id}", response_model=AccountOut)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    return service.delete_account(db, account_id)
