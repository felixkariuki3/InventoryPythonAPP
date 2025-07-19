from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.crud import stock_transaction as transaction_crud
from backend.schemas import stock_transaction as transaction_schema
from backend.schemas.stock_transaction import TransferTransaction

router = APIRouter(prefix="/transactions", tags=["transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=transaction_schema.TransactionOut)
def create_transaction(txn: transaction_schema.TransactionCreate, db: Session = Depends(get_db)):
    return transaction_crud.create_transaction(db, txn)

@router.get("/", response_model=list[transaction_schema.TransactionOut])
def list_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return transaction_crud.get_transactions(db, skip, limit)

@router.get("/logs", response_model=list[transaction_schema.InventoryLogOut])
def list_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return transaction_crud.get_logs(db, skip, limit)

@router.post("/transfer")
def transfer_items(txn: TransferTransaction, db: Session = Depends(get_db)):
    return transaction_crud.create_transfer(db, txn)

@router.post("/issue", response_model=transaction_schema.TransactionOut)
def issue_item(txn: transaction_schema.IssueCreate, db: Session = Depends(get_db)):
    return transaction_crud.create_issue(db, txn)
