# backend/crud/wip.py
from sqlalchemy.orm import Session
from backend.models.wip import WorkInProgress
from backend.schemas.wip import WIPCreate, WIPUpdate
from backend.models.production_order import ProductionOrder
from fastapi import HTTPException
from datetime import datetime
from backend.models.item import Item


def create_wip(db: Session, wip_data: WIPCreate) -> WorkInProgress:
    order = db.query(ProductionOrder).filter_by(id=wip_data.production_order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production Order not found")

    # Corrected: Fetch item using order.item_id (not class name)
    wip_item = db.query(Item).filter_by(item_id=order.item_id).first()
    if not wip_item:
        raise HTTPException(status_code=404, detail="Production item not found")

    # Ensure values are floats for arithmetic
    try:
        cost_per_unit = float(wip_item.average_cost or 0.0)
        issued_quantity = float(wip_data.issued_quantity)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid numeric values in WIP data")

    total_cost = cost_per_unit * issued_quantity

    wip = WorkInProgress(
        production_order_id=wip_data.production_order_id,
        issued_quantity=issued_quantity,
        completed_quantity=0.0,
        status="in_progress",
        item_id=order.item_id,
        cost_per_unit=cost_per_unit,
        total_cost=total_cost,
        updated_at=datetime.utcnow()
    )

    db.add(wip)
    db.commit()
    db.refresh(wip)
    return wip



def update_wip(db: Session, wip_id: int, update_data: WIPUpdate) -> WorkInProgress:
    wip = db.query(WorkInProgress).filter_by(id=wip_id).first()
    if not wip:
        raise HTTPException(status_code=404, detail="WIP entry not found")

    wip.completed_quantity = update_data.completed_quantity
    wip.status = update_data.status
    wip.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(wip)
    return wip


def get_wip_by_order_id(db: Session, order_id: int) -> WorkInProgress | None:
    return db.query(WorkInProgress).filter_by(production_order_id=order_id).first()
