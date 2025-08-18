from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.models.production_order import ProductionOrder, ProductionStatus
from backend.models.item import Item
from backend.models.bom import BOM
from backend.models.wip import WorkInProgress
from backend.services.items import get_item
from backend.services.bom import get_bom_for_item
from backend.services.inventory_service import adjust_inventory  # <-- new core service
from utils.costing import calculate_weighted_average
from backend.logging_config import logger


def start_production_order(db: Session, order_id: int):
    """
    Simply marks the order as started and creates a WIP record.
    Actual issuing of materials happens in `issue_materials_for_production`.
    """
    order = db.query(ProductionOrder).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")

    bom_components = db.query(BOM).filter(BOM.parent_item_id == order.item_id).all()
    if not bom_components:
        raise HTTPException(status_code=400, detail="No BOM found for this item")

    # Create a single WIP entry marker
    wip = WorkInProgress(production_order_id=order.id)
    db.add(wip)

    order.status = ProductionStatus.in_progress
    db.commit()
    logger.info("Started production order ID %s", order_id)


def issue_materials_for_production(db: Session, production_order_id: int):
    """
    Issues all BOM components to WIP (consumes raw material stock).
    """
    order = db.query(ProductionOrder).filter(ProductionOrder.id == production_order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")

    bom_items = get_bom_for_item(db, order.item_id)
    if not bom_items:
        raise HTTPException(status_code=400, detail="No BOM for this item")

    for bom_item in bom_items:
        qty_to_issue = bom_item.quantity * order.quantity
        item_record = get_item(db, bom_item.component_item_id)

        if not item_record:
            logger.error("Item not found for component ID %s", bom_item.component_item_id)
            continue

        cost_per_unit = item_record.average_cost or 0.0
        total_cost = qty_to_issue * cost_per_unit

        # Issue from inventory (negative movement)
        adjust_inventory(
            db,
            item_id=item_record.item_id,
            warehouse_id=1,   # or order.source_warehouse_id if defined
            qty=qty_to_issue,
            txn_type="issue",
            reference=f"Production Order #{order.id}",
            note="issue-for-production",
        )

        # Record WIP entry
        wip_entry = WorkInProgress(
            production_order_id=order.id,
            item_id=item_record.item_id,
            issued_quantity=qty_to_issue,
            cost_per_unit=cost_per_unit,
            total_cost=total_cost,
            completed_quantity=0.0,
            status="in_progress",
            updated_at=datetime.utcnow()
        )
        db.add(wip_entry)

    db.commit()
    logger.info("Issued materials for production order ID %s", order.id)


def complete_production_order(db: Session, order_id: int, completed_quantity: float):
    """
    Completes a production order:
    - Closes WIP
    - Calculates unit cost from consumed WIP
    - Receives finished goods into stock (with cost update)
    """
    order = db.query(ProductionOrder).filter_by(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production order not found")

    wip_entries = db.query(WorkInProgress).filter_by(production_order_id=order.id).all()
    if not wip_entries:
        raise HTTPException(status_code=400, detail="No WIP entries for this order")

    if completed_quantity <= 0:
        raise HTTPException(status_code=400, detail="Completed quantity must be greater than 0")

    order.quantity = completed_quantity
    order.status = ProductionStatus.completed
    order.end_date = datetime.utcnow()

    total_wip_cost = sum(w.total_cost for w in wip_entries)
    cost_per_unit = total_wip_cost / completed_quantity

    # Receive finished goods into inventory with cost update
    adjust_inventory(
        db,
        item_id=order.item_id,
        warehouse_id=1,  # or order.target_warehouse_id if defined
        qty=completed_quantity,
        txn_type="receipt",
        reference=f"Production Order #{order.id}",
        unit_cost=cost_per_unit,
        note="production-receipt",
    )

    db.commit()
    logger.info("Completed production order ID %s with quantity %s", order.id, completed_quantity)
