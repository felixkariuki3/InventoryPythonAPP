# backend/crud/production_order.py

from sqlalchemy.orm import Session
from backend.models.production_order import ProductionOrder, OrderStatus
from backend.schemas.production_order import ProductionOrderCreate

def create_order(db: Session, order_data: ProductionOrderCreate):
    order = ProductionOrder(**order_data.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_all_orders(db: Session):
    return db.query(ProductionOrder).all()

def update_order_status(db: Session, order_id: int, status: OrderStatus):
    order = db.query(ProductionOrder).get(order_id)
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
    return order
