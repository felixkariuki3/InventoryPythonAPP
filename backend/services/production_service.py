from sqlalchemy.orm import Session
from backend.models import production_order, item, stock_transaction, bom
from backend.models.wip import WorkInProgress
from backend.models.inventory import InventoryTransaction
from backend.services.items import get_item
from backend.services.inventory import update_inventory_quantity
from backend.services.bom import get_bom_for_item
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

    # services/production.py

def issue_materials_for_production(db, production_order):
    bom_items = get_bom_for_item(db, production_order.item_id)
    for bom_item in bom_items:
        # 1. Calculate quantity to issue
        qty_to_issue = bom_item.quantity * production_order.quantity
        
        # 2. Fetch current cost
        item = get_item(db, bom_item.component_item_id)
        cost_per_unit = item.average_cost or 0.0
        total_cost = qty_to_issue * cost_per_unit
        
        # 3. Reduce inventory
        update_inventory_quantity(db, item.id, -qty_to_issue)
        
        # 4. Log to WIP
        wip_entry = WorkInProgress(
            production_order_id=production_order.id,
            item_id=item.item.id,
            quantity_issued=qty_to_issue,
            cost_per_unit=cost_per_unit,
            total_cost=total_cost
        )
        db.add(wip_entry)
    
    db.commit()


def complete_production_order(db: Session, order_id: int, completed_quantity: float):
    order = db.query(production_order.ProductionOrder).filter_by(id=order_id).first()
    if not order or not order.wip:
        raise Exception("Production order or WIP not found.")

    order.wip.completed_quantity = completed_quantity
    order.status = production_order.ProductionStatus.completed
    order.end_date = datetime.utcnow()

    # 1. Calculate total WIP cost for this order
    wip_entries = db.query(WorkInProgress).filter_by(production_order_id=order.id).all()
    total_wip_cost = sum(w.total_cost for w in wip_entries)

    # 2. Determine unit cost of finished goods
    if completed_quantity <= 0:
        raise Exception("Completed quantity must be greater than 0 to calculate unit cost.")
    cost_per_unit = total_wip_cost / completed_quantity

    # 3. Log inventory receipt transaction
    db.add(InventoryTransaction(
        item_id=order.item_id,
        warehouse_id=1,
        quantity=completed_quantity,
        transaction_type="receipt",
        reference=f"Production Order #{order.id}",
    ))

    # 4. Log inventory change (your custom log)
    db.add(stock_transaction.InventoryLog(
        item_id=order.item_id,
        warehouse_id=1,
        transaction_id=0,
        change=completed_quantity,
        note=f"Produced from Production Order #{order.id}",
        timestamp=datetime.utcnow()
    ))

    # 5. Update item quantity and average cost
    item_record = db.query(item.Item).filter_by(id=order.item_id).first()
    current_qty = item_record.quantity or 0
    current_cost = item_record.average_cost or 0.0
    item_record.quantity += completed_quantity
    item_record.average_cost = calculate_weighted_average(
        current_qty, current_cost,
        completed_quantity, cost_per_unit
    )

    db.commit()
