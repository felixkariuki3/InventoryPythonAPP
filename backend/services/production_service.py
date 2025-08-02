from sqlalchemy.orm import Session
from backend.models import production_order, item, stock_transaction, bom
from backend.models.wip import WorkInProgress
from backend.models.inventory import InventoryTransaction
from utils.costing import calculate_weighted_average
from datetime import datetime

def start_production_order(db: Session, order_id: int):
    order = db.query(production_order.ProductionOrder).filter_by(id=order_id).first()
    if not order:
        raise Exception("Production order not found.")

    bom_components = db.query(bom.BOM).filter(bom.BOM.parent_item_id == order.item_id).all()
    if not bom_components:
        raise Exception("No BOM found for this item.")

    for component in bom_components:
        qty_needed = component.quantity * order.quantity
        db.add(InventoryTransaction(
            item_id=component.component_item_id,
            warehouse_id=1,
            quantity=-qty_needed,
            transaction_type="issue",
            reference=f"Production Order #{order.id}",
        ))
        db.add(stock_transaction.InventoryLog(
            item_id=component.component_item_id,
            warehouse_id=1,
            transaction_id=0,  # Replace later if needed
            change=-qty_needed,
            note=f"Issue for Production Order #{order.id}",
            timestamp=datetime.utcnow()
        ))
        item_record = db.query(item.Item).filter_by(id=component.component_item_id).first()
        item_record.quantity -= qty_needed

    # Start tracking
    wip = WorkInProgress(production_order_id=order.id)
    db.add(wip)
    order.status = production_order.ProductionStatus.in_progress

    db.commit()

def complete_production_order(db: Session, order_id: int, completed_quantity: float):
    order = db.query(production_order.ProductionOrder).filter_by(id=order_id).first()
    if not order or not order.wip:
        raise Exception("Production order or WIP not found.")

    order.wip.completed_quantity = completed_quantity
    order.status = production_order.ProductionStatus.completed
    order.end_date = datetime.utcnow()

    db.add(InventoryTransaction(
        item_id=order.item_id,
        warehouse_id=1,
        quantity=completed_quantity,
        transaction_type="receipt",
        reference=f"Production Order #{order.id}",
    ))
    db.add(stock_transaction.InventoryLog(
        item_id=order.item_id,
        warehouse_id=1,
        transaction_id=0,
        change=completed_quantity,
        note=f"Produced from Production Order #{order.id}",
        timestamp=datetime.utcnow()
    ))

    item_record = db.query(item.Item).filter_by(id=order.item_id).first()
    current_qty = item_record.quantity or 0
    current_cost = item_record.average_cost or 0.0
    received_cost = current_cost  # You can enhance this later

    item_record.quantity += completed_quantity
    item_record.average_cost = calculate_weighted_average(current_qty, current_cost, completed_quantity, received_cost)

    db.commit()
