# backend/services/purchasing.py
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from sqlalchemy import inspect
from sqlalchemy.orm.state import InstanceState
from fastapi import HTTPException
from backend.models.purchase import PurchaseOrder, PurchaseOrderLine,PurchaseOrderStatus
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
        change=qty,
        note=note,
    )
    db.add(log)
    return log

from fastapi import HTTPException
from backend.models.purchase import PurchaseOrder, PurchaseOrderStatus

def receive_purchase_order(db, order_id: int, receipts: list[dict]):
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    fully_received = True  # assume complete until proven otherwise

    for receipt in receipts:
        line = next((l for l in order.lines if l.id == receipt["line_id"]), None)
        if not line:
            raise HTTPException(status_code=404, detail=f"Line {receipt['line_id']} not found")

        line.received_qty += receipt["received_qty"]

        # check if this line is fully received
        if line.received_qty < line.ordered_qty:
            fully_received = False

    # update order status
    if fully_received:
        order.status = PurchaseOrderStatus.RECEIVED
    else:
        order.status = PurchaseOrderStatus.PARTIALLY_RECEIVED

    db.commit()
    db.refresh(order)
    return order