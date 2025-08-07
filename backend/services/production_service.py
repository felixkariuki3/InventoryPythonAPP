from sqlalchemy.orm import Session
from backend.models.production_order import ProductionOrder, ProductionStatus
from backend.models.item import Item
from backend.models.stock_transaction import InventoryLog, Transaction
from backend.models.bom import BOM
from backend.models.wip import WorkInProgress
from backend.models.inventory import InventoryTransaction
from backend.services.items import get_item
from backend.services.inventory import update_inventory_quantity
from backend.services.bom import get_bom_for_item
from utils.costing import calculate_weighted_average
from datetime import datetime
from backend.logging_config import logger


def start_production_order(db: Session, order_id: int):
    order = db.query(ProductionOrder).filter_by(id=order_id).first()
    if not order:
        raise Exception("Production order not found.")

    bom_components = db.query(BOM).filter(BOM.parent_item_id == order.item_id).all()
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
        db.add(InventoryLog(
            item_id=component.component_item_id,
            warehouse_id=1,
            transaction_id=0,
            change=-qty_needed,
            note=f"Issue for Production Order #{order.id}",
            timestamp=datetime.utcnow()
        ))
        item_record = db.query(Item).filter_by(id=component.component_item_id).first()
        item_record.quantity -= qty_needed

    wip = WorkInProgress(production_order_id=order.id)
    db.add(wip)
    order.status = ProductionStatus.in_progress
    db.commit()
    logger.info("Started production order ID %s", order_id)


def issue_materials_for_production(db: Session, production_order: ProductionOrder):
    bom_items = get_bom_for_item(db, production_order.item_id)

    for bom_item in bom_items:
        qty_to_issue = bom_item.quantity * production_order.quantity
        item_record = get_item(db, bom_item.component_item_id)

        if not item_record:
            logger.error("Item not found for component ID %s", bom_item.component_item_id)
            continue

        cost_per_unit = item_record.average_cost or 0.0
        total_cost = qty_to_issue * cost_per_unit

        update_inventory_quantity(db, item_record.id, -qty_to_issue)

        wip_entry = WorkInProgress(
            production_order_id=production_order.id,
            item_id=item_record.id,
            issued_quantity=qty_to_issue,
            cost_per_unit=cost_per_unit,
            total_cost=total_cost,
            completed_quantity=0.0,
            status="in_progress",
            updated_at=datetime.utcnow()
        )
        db.add(wip_entry)

    db.commit()
    logger.info("Issued materials for production order ID %s", production_order.id)


def complete_production_order(db: Session, order_id: int, completed_quantity: float):
    order = db.query(ProductionOrder).filter_by(id=order_id).first()
    if not order or not order.wip:
        raise Exception("Production order or WIP not found.")

    order.quantity = completed_quantity
    order.status = ProductionStatus.completed
    order.end_date = datetime.utcnow()

    wip_entries = db.query(WorkInProgress).filter_by(production_order_id=order.id).all()
    total_wip_cost = sum(w.total_cost for w in wip_entries)

    if completed_quantity <= 0:
        raise Exception("Completed quantity must be greater than 0 to calculate unit cost.")
    cost_per_unit = total_wip_cost / completed_quantity

    db.add(InventoryTransaction(
        item_id=order.item_id,
        warehouse_id=1,
        quantity=completed_quantity,
        transaction_type="receipt",
        reference=f"Production Order #{order.id}",
    ))

    db.add(InventoryLog(
        item_id=order.item_id,
        warehouse_id=1,
        transaction_id=0,
        change=completed_quantity,
        note=f"Produced from Production Order #{order.id}",
        timestamp=datetime.utcnow()
    ))

    item_record = db.query(Item).filter_by(id=order.item_id).first()
    current_qty = item_record.quantity or 0
    current_cost = item_record.average_cost or 0.0
    item_record.quantity += completed_quantity
    item_record.average_cost = calculate_weighted_average(
        current_qty, current_cost,
        completed_quantity, cost_per_unit
    )

    db.commit()
    logger.info("Completed production order ID %s with quantity %s", order.id, completed_quantity)
