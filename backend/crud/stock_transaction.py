from sqlalchemy.orm import Session
from backend.models.stock_transaction import Transaction, InventoryLog
from backend.schemas.stock_transaction import TransactionCreate
from fastapi import HTTPException

def create_transaction(db: Session, txn: TransactionCreate):
    if txn.type not in ['receipt', 'issue', 'transfer', 'adjustment']:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    change = txn.quantity if txn.type in ['receipt', 'adjustment'] else -txn.quantity
    if txn.type == 'transfer':
        raise HTTPException(status_code=400, detail="Use the transfer endpoint for transfers")

    db_txn = Transaction(**txn.dict())
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)

    # Log inventory change
    log = InventoryLog(
        item_id=txn.item_id,
        warehouse_id=txn.warehouse_id,
        transaction_id=db_txn.id,
        change=change,
        note=txn.type
    )
    db.add(log)
    db.commit()

    return db_txn

def get_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Transaction).offset(skip).limit(limit).all()

def get_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(InventoryLog).offset(skip).limit(limit).all()
