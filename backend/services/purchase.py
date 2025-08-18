# backend/services/purchasing.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.purchase import PurchaseOrder, PurchaseOrderLine
from backend.models.item import Item
from backend.models.stock_transaction import InventoryLog
from utils.costing import calculate_weighted_average


def update_item_stock(db: Session, item: Item, qty_received: float, unit_cost: float):
    """
    Updates the stock level and weighted average cost of an item.
    """
    current_qty = item.quantity or 0
    current_cost = item.average_cost or 0.0

    new_avg = calculate_weighted_average(
        current_qty, current_cost,
        qty_received, unit_cost
    )

    item.quantity = current_qty + qty_received
    item.average_cost = new_avg
    db.add(item)
    return item


def log_inventory_movement(db: Session, item_id: int, warehouse_id: int, qty: float, note: str):
    """
    Creates an inventory log entry.
    """
    log = InventoryLog(
        item_id=item_id,
        warehouse_id=warehouse_id,
        quantity=qty,
        note=note
    )
    db.add(log)
    return log


def receive_purchase_order(db: Session, order_id: int):
    """
    Receives a purchase order, updates stock levels, 
    recalculates weighted average costs, and logs inventory movements.
    """
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    if order.status != "open":
        raise HTTPException(status_code=400, detail=f"Order already in {order.status}")

    if not order.lines or len(order.lines) == 0:
        raise HTTPException(status_code=400, detail="Order has no lines")

    if order.status == "received":
        raise HTTPException(status_code=400, detail="Purchase order already received")

    for line in order.lines:
        item = db.query(Item).filter(Item.item_id == line.item_id).first()

        if not item:
            continue  # Or raise HTTPException if strict

        # 1. Update stock
        update_item_stock(db, item, line.quantity, line.unit_cost)

        # 2. Log movement
        log_inventory_movement(
            db=db,
            item_id=item.item_id,
            warehouse_id=item.warehouse_id,  # if tracked
            qty=line.quantity,
            note=f"PO #{order.id} received"
        )

    order.status = "received"
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
