# backend/services/inventory_service.py

from typing import Optional, Literal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from backend.models.item import Item
from backend.models.stock_transaction import Transaction, InventoryLog
from backend.models.inventory import InventoryTransaction  # used here as per-warehouse balance row
from utils.costing import calculate_weighted_average
from backend.logging_config import logger

TxnType = Literal["receipt", "issue", "adjustment", "transfer"]

def _get_wh_balance(db: Session, item_id: int, warehouse_id: int) -> float:
    """
    Compute current on-hand for (item, warehouse) from InventoryLog.
    This matches how you're already validating transfers.
    """
    qty = db.query(func.coalesce(func.sum(InventoryLog.change), 0.0)).filter(
        InventoryLog.item_id == item_id,
        InventoryLog.warehouse_id == warehouse_id
    ).scalar()
    return float(qty or 0.0)

def _upsert_balance_row(db: Session, item_id: int, warehouse_id: int) -> InventoryTransaction:
    """
    Treat InventoryTransaction as the 'per-warehouse balance' row (as in your current code).
    If you later create a dedicated InventoryBalance model, swap it here.
    """
    row = db.query(InventoryTransaction).filter_by(
        item_id=item_id, warehouse_id=warehouse_id
    ).first()
    if not row:
        row = InventoryTransaction(
            item_id=item_id,
            warehouse_id=warehouse_id,
            quantity=0.0
        )
        db.add(row)
        db.flush()
    return row

def get_on_hand(db: Session, item_id: int, warehouse_id: int) -> float:
    """Public helper if you need it elsewhere (UI endpoints, etc.)."""
    return _get_wh_balance(db, item_id, warehouse_id)

def adjust_inventory(
    db: Session,
    *,
    item_id: int,
    warehouse_id: int,
    qty: float,
    txn_type: TxnType,
    reference: Optional[str] = None,
    unit_cost: Optional[float] = None,   # cost per unit for receipts (for WAC)
    note: Optional[str] = None,
    allow_negative: bool = False,
) -> dict:
    """
    Core, atomic adjustment. Positive qty for receipts/adjustment up; negative for issue/transfer-out.
    - Creates Transaction (+ optional unit_cost)
    - Creates InventoryLog
    - Updates per-warehouse balance row (InventoryTransaction.quantity)
    - Updates Item.quantity (global) and Item.average_cost for receipts (WAC)
    """

    if txn_type not in ("receipt", "issue", "adjustment", "transfer"):
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    if qty == 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be zero")

    # normalize sign by type (lets callers pass positive numbers)
    signed_qty = qty
    if txn_type in ("issue", "transfer"):
        signed_qty = -abs(qty)
    elif txn_type in ("receipt", "adjustment"):
        signed_qty = abs(qty)

    item = db.query(Item).filter(Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    with db.begin():  # atomic block (SQLite-friendly)
        # Validate stock for outbound moves
        if signed_qty < 0 and not allow_negative:
            on_hand = _get_wh_balance(db, item_id, warehouse_id)
            if on_hand + signed_qty < 0:
                raise HTTPException(status_code=400, detail="Insufficient stock")

        # Upsert per-warehouse balance row and apply change
        bal_row = _upsert_balance_row(db, item_id, warehouse_id)
        bal_row.quantity = (bal_row.quantity or 0.0) + signed_qty

        # Update item total quantity (aggregate view)
        item.quantity = (item.quantity or 0.0) + signed_qty

        # Weighted Average Cost update only on RECEIPT with cost info
        if txn_type == "receipt" and unit_cost is not None:
            old_qty = (item.quantity or 0.0) - signed_qty  # previous qty before this receipt
            old_cost = item.average_cost or 0.0
            item.average_cost = calculate_weighted_average(
                old_qty, old_cost,
                abs(signed_qty), float(unit_cost)
            )

        # Create Transaction record
        txn = Transaction(
            item_id=item_id,
            warehouse_id=warehouse_id,
            type=txn_type,
            quantity=abs(signed_qty),              # store magnitude; sign is implied by type
            reference=reference,
            unit_cost=unit_cost,                   # you added this column in your migration
            created_at=datetime.utcnow() if hasattr(Transaction, "created_at") else None
        )
        db.add(txn)
        db.flush()  # so we can reference txn.id in the log

        # Audit log with explicit signed change
        log = InventoryLog(
            item_id=item_id,
            warehouse_id=warehouse_id,
            transaction_id=txn.id,
            change=signed_qty,
            note=note or txn_type,
            timestamp=datetime.utcnow() if hasattr(InventoryLog, "timestamp") else None
        )
        db.add(log)

        # SQLAlchemy will commit at the end of `with db.begin()`

    logger.info(
        "Inventory %s: item=%s wh=%s qty=%s ref=%s cost=%s new_wh_bal=%.4f new_item_qty=%.4f",
        txn_type, item_id, warehouse_id, qty, reference, unit_cost,
        bal_row.quantity, item.quantity
    )
    return {
        "status": "success",
        "transaction_id": txn.id,
        "log_id": log.id,
        "new_warehouse_balance": bal_row.quantity,
        "new_item_quantity": item.quantity,
        "average_cost": item.average_cost,
    }

def transfer_inventory(
    db: Session,
    *,
    item_id: int,
    source_warehouse_id: int,
    destination_warehouse_id: int,
    qty: float,
    reference: Optional[str] = None
) -> dict:
    """
    Atomic transfer: issue from source, receipt to destination.
    """
    if source_warehouse_id == destination_warehouse_id:
        raise HTTPException(status_code=400, detail="Source and destination must be different")

    with db.begin():
        # issue (outbound)
        out_res = adjust_inventory(
            db,
            item_id=item_id,
            warehouse_id=source_warehouse_id,
            qty=qty,
            txn_type="transfer",
            reference=reference,
            note="transfer-out",
        )
        # receipt (inbound) – transfers don’t change WAC, so no unit_cost
        in_res = adjust_inventory(
            db,
            item_id=item_id,
            warehouse_id=destination_warehouse_id,
            qty=qty,
            txn_type="receipt",
            reference=reference,
            note="transfer-in",
        )

    return {
        "status": "success",
        "issued_transaction_id": out_res["transaction_id"],
        "received_transaction_id": in_res["transaction_id"],
        "source_new_balance": out_res["new_warehouse_balance"],
        "destination_new_balance": in_res["new_warehouse_balance"],
    }
