# backend/crud/production.py
from sqlalchemy.orm import Session
from backend.models import production_order as models
from backend.schemas import production_order as schemas


def create_production_order(db: Session, order: schemas.ProductionOrderCreate):
    db_order = models.ProductionOrder(
        item_id=order.item_id,
        quantity=order.quantity,
        status=models.ProductionStatus.planned
    )
    db.add(db_order)
    db.flush()

    for op in order.operations:
        db_op = models.ProductionOperation(
            order_id=db_order.id,
            name=op.name,
            sequence=op.sequence,
            duration_minutes=op.duration_minutes
        )
        db.add(db_op)

    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(db: Session):
    return db.query(models.ProductionOrder).all()
