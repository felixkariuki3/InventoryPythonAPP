# backend/crud/wip.py
from sqlalchemy.orm import Session
from backend.models.wip import WorkInProgress
from backend.schemas.wip import WIPCreate, WIPUpdate
from backend.models.production_order import ProductionOrder
from fastapi import HTTPException
from datetime import datetime


def create_wip(db: Session, wip_data: WIPCreate) -> WorkInProgress:
    order = db.query(ProductionOrder).filter_by(id=wip_data.production_order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Production Order not found")

    wip = WorkInProgress(
        production_order_id=wip_data.production_order_id,
        issued_quantity=wip_data.issued_quantity,
        completed_quantity=0.0,
        status="in_progress"
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
