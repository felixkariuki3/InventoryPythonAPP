# backend/services/purchasing.py
from sqlalchemy.orm import Session
from backend.models.purchase import PurchaseOrder, PurchaseOrderLine
from backend.models.item import Item
from utils.costing import calculate_weighted_average
from fastapi import HTTPException
from backend.models.stock_transaction import InventoryLog

def receive_purchase_order(db: Session, order_id: int):
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    if order.status != "open":
        raise HTTPException(status_code=400, detail=f"Order already in {order.status}")
    
    if not order.lines or len(order.lines) == 0:
        raise HTTPException(status_code=400, detail="Order has no lines")

    if order.status == "received":
        raise HTTPException(status_code=400, detail="Purchase order already received")

    for line in PurchaseOrder.lines:
        item = db.query(Item).filter(Item.item_id == PurchaseOrderLine.item_id).first()

        if not item:
            continue  # Or raise an error depending on your design

        # Update inventory quantity and average cost
        current_qty = item.quantity or 0
        current_cost = item.average_cost or 0.0
        new_avg = calculate_weighted_average(current_qty, current_cost, PurchaseOrderLine.quantity, PurchaseOrderLine.unit_cost)

        item.quantity = current_qty + PurchaseOrderLine.quantity
        item.average_cost = new_avg

        db.add(item)

        InventoryLog(
        db=db,
        item_id=item.item_id,
        warehouse_id=item.warehouse_id,  # Replace with actual warehouse if tracked
        quantity=PurchaseOrderLine.quantity,
        note=f"PO #{order.id} received"
        )
    order.status = "received"
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
