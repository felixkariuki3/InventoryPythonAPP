from sqlalchemy.orm import Session
from backend.models.stock_transaction import Transaction, InventoryLog
from backend.schemas.stock_transaction import TransactionCreate
from fastapi import HTTPException
from backend.schemas.stock_transaction import TransferTransaction
from backend.schemas.stock_transaction import TransactionCreate
from backend.schemas import stock_transaction as transaction_schema
from sqlalchemy import func
from backend.models.inventory import InventoryTransaction





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
    return db_txn

def create_transfer(db: Session, txn: TransferTransaction):
    
    # To validate destination Warehouse
    if txn.source_warehouse_id == txn.destination_warehouse_id:
        raise HTTPException(status_code=400, detail="Source and destination must be different")
    
    # To validate source quantity
    total = db.query(func.sum(InventoryLog.change)).filter(
    InventoryLog.item_id == txn.item_id,
    InventoryLog.warehouse_id == txn.source_warehouse_id
    ).scalar() or 0

    if total < txn.quantity:
        raise HTTPException(status_code=400, detail="Insufficient quantity in source warehouse")

    # Create debit (issue) transaction
    issue_txn = Transaction(
        item_id=txn.item_id,
        warehouse_id=txn.source_warehouse_id,
        type="transfer",
        quantity=-txn.quantity,
        reference=txn.reference
    )
    db.add(issue_txn)
    db.flush()

    # Log issue
    issue_log = InventoryLog(
        item_id=txn.item_id,
        warehouse_id=txn.source_warehouse_id,
        transaction_id=issue_txn.id,
        change=-txn.quantity,
        note="transfer-out"
    )
    db.add(issue_log)

    # Create credit (receipt) transaction
    receipt_txn = Transaction(
        item_id=txn.item_id,
        warehouse_id=txn.destination_warehouse_id,
        type="transfer",
        quantity=txn.quantity,
        reference=txn.reference
    )
    db.add(receipt_txn)
    db.flush()

    # Log receipt
    receipt_log = InventoryLog(
        item_id=txn.item_id,
        warehouse_id=txn.destination_warehouse_id,
        transaction_id=receipt_txn.id,
        change=txn.quantity,
        note="transfer-in"
    )
    db.add(receipt_log)

    db.commit()

    return {"status": "success", "issued_transaction_id": issue_txn.id, "received_transaction_id": receipt_txn.id}

def create_issue(db: Session, txn: transaction_schema.IssueCreate):
    item_wh = db.query(InventoryTransaction).filter_by(
        item_id=txn.item_id,
        warehouse_id=txn.warehouse_id
        
    ).first()
    print("Trying to find Inventory with item_id =", txn.item_id, "and warehouse_id =", txn.warehouse_id)

    if not item_wh or item_wh.quantity < txn.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    item_wh.quantity -= txn.quantity
    db.commit()
    db.refresh(item_wh)
    
    db_txn = Transaction(
        item_id=txn.item_id,
        warehouse_id=txn.warehouse_id,
        type="issue",
        quantity=txn.quantity,
        reference=txn.reference,
    )
    db.add(db_txn)
    db.flush() 

    log = InventoryLog(
        item_id=txn.item_id,
        warehouse_id=txn.warehouse_id,
        change=-txn.quantity,
        note="issue",
        transaction_id=db_txn.id,
    )
    db.add(log)
    db.commit()
    return log

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
