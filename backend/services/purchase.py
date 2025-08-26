# backend/services/purchasing.py
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from sqlalchemy import inspect
from sqlalchemy.orm.state import InstanceState
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
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


def log_inventory_movement(db: Session, item_id: int, warehouse_id: int, qty: float, note: str,transaction_id:int):
    """
    Creates an inventory log entry.
    """
    log = InventoryLog(
        item_id=item_id,
        warehouse_id=warehouse_id,
        change=qty,
        transaction_id=transaction_id,
        note=note,
    )
    db.add(log)
    return log

from backend.models.purchase import PurchaseOrder, PurchaseOrderStatus
from backend.schemas.purchase import ReceiptLine



def receive_purchase_order(db: Session, order_id: int, receipts: list[ReceiptLine]):
    try:
        order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Purchase order not found")

        fully_received = True  # assume complete until proven otherwise

        for receipt in receipts:
            line = next((l for l in order.lines if l.id == receipt.id), None)
            if not line:
                raise HTTPException(status_code=400, detail=f"Line {receipt.id} not found in order {order_id}")
         # Strict check: prevent receiving more than ordered
            if line.received_qty + receipt.received_qty > line.quantity:
                raise HTTPException(
                status_code=400,
                detail=(
                    f"Cannot receive more than ordered for line {line.id}. "
                    f"Ordered: {line.quantity}, Already received: {line.received_qty}, "
                    f"Tried to receive: {receipt.received_qty}"
                )
            )
            # Update received qty
            line.received_qty = (line.received_qty or 0) + receipt.received_qty

            # Update item stock & average cost
            item = db.query(Item).filter(Item.item_id == line.item_id).first()
            if not item:
                raise HTTPException(status_code=404, detail=f"Item {line.item_id} not found")

            update_item_stock(db, item, receipt.received_qty, line.unit_cost)

            # Log inventory movement
            log_inventory_movement(
                db,
                item_id=line.item_id,
                warehouse_id=line.warehouse_id,
                qty=receipt.received_qty,
                transaction_id =line.id,
                note=f"PO#{order.id} - Receipt for line {line.id}"
            )

            # If not fully received
            if line.received_qty < line.quantity:
                fully_received = False

        # update order status
        order.status = (
            PurchaseOrderStatus.RECEIVED if fully_received
            else PurchaseOrderStatus.PARTIALLY_RECEIVED
        )

        db.commit()
        db.refresh(order)
        return order

    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")