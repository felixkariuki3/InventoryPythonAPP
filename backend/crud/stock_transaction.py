from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from backend.models.stock_transaction import Transaction, InventoryLog
from backend.models.inventory import InventoryTransaction
from backend.schemas import stock_transaction as transaction_schema


def create_transaction(db: Session, txn: transaction_schema.TransactionCreate):
    if txn.type not in ['receipt', 'issue', 'adjustment']:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    # Get or create inventory record
    item_wh = db.query(InventoryTransaction).filter_by(
        item_id=txn.item_id, warehouse_id=txn.warehouse_id
    ).first()

    if not item_wh:
        if txn.type == "issue":
            raise HTTPException(status_code=400, detail="No stock available for issue")
        # create inventory record for receipt/adjustment
        item_wh = InventoryTransaction(
            item_id=txn.item_id, warehouse_id=txn.warehouse_id, quantity=0
        )
        db.add(item_wh)
        db.flush()

    # Apply stock change
    change = txn.quantity if txn.type in ['receipt', 'adjustment'] else -txn.quantity
    if txn.type == "issue" and item_wh.quantity < txn.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    item_wh.quantity += change

    # Create transaction record
    db_txn = Transaction(**txn.dict())
    db.add(db_txn)
    db.flush()

    # Create inventory log
    log = InventoryLog(
        item_id=txn.item_id,
        warehouse_id=txn.warehouse_id,
        transaction_id=db_txn.id,
        change=change,
        note=txn.type,
    )
    db.add(log)

    db.commit()
    db.refresh(item_wh)
    return db_txn


def create_transfer(db: Session, txn: transaction_schema.TransferTransaction):
    if txn.source_warehouse_id == txn.destination_warehouse_id:
        raise HTTPException(status_code=400, detail="Source and destination must be different")

    # Validate stock in source
    source_inv = db.query(InventoryTransaction).filter_by(
        item_id=txn.item_id, warehouse_id=txn.source_warehouse_id
    ).first()
    if not source_inv or source_inv.quantity < txn.quantity:
        raise HTTPException(status_code=400, detail="Insufficient quantity in source warehouse")

    # Get/create destination inventory
    dest_inv = db.query(InventoryTransaction).filter_by(
        item_id=txn.item_id, warehouse_id=txn.destination_warehouse_id
    ).first()
    if not dest_inv:
        dest_inv = InventoryTransaction(
            item_id=txn.item_id, warehouse_id=txn.destination_warehouse_id, quantity=0
        )
        db.add(dest_inv)
        db.flush()

    # Update stock
    source_inv.quantity -= txn.quantity
    dest_inv.quantity += txn.quantity

    # Create issue txn & log
    issue_txn = Transaction(
        item_id=txn.item_id, warehouse_id=txn.source_warehouse_id,
        type="transfer", quantity=-txn.quantity, reference=txn.reference
    )
    db.add(issue_txn)
    db.flush()
    issue_log = InventoryLog(
        item_id=txn.item_id, warehouse_id=txn.source_warehouse_id,
        transaction_id=issue_txn.id, change=-txn.quantity, note="transfer-out"
    )
    db.add(issue_log)

    # Create receipt txn & log
    receipt_txn = Transaction(
        item_id=txn.item_id, warehouse_id=txn.destination_warehouse_id,
        type="transfer", quantity=txn.quantity, reference=txn.reference
    )
    db.add(receipt_txn)
    db.flush()
    receipt_log = InventoryLog(
        item_id=txn.item_id, warehouse_id=txn.destination_warehouse_id,
        transaction_id=receipt_txn.id, change=txn.quantity, note="transfer-in"
    )
    db.add(receipt_log)

    db.commit()

    return {
        "status": "success",
        "issued_transaction_id": issue_txn.id,
        "received_transaction_id": receipt_txn.id
    }


def get_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Transaction).offset(skip).limit(limit).all()


def get_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(InventoryLog).offset(skip).limit(limit).all()
