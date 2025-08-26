from sqlalchemy.orm import Session
from backend.models.sales import SalesOrder, SalesOrderLine
from backend.schemas.sales import (
    SalesOrderCreate, SalesOrderUpdate,
    SalesOrderLineCreate
)

# ---- Sales Order CRUD ----
def create_sales_order(db: Session, order: SalesOrderCreate):
    db_order = SalesOrder(
        customer_id=order.customer_id,
        order_date=order.order_date,
        due_date=order.due_date,
        status=order.status or "draft",
        total_amount=0.0
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_sales_order(db: Session, order_id: int):
    return db.query(SalesOrder).filter(SalesOrder.id == order_id).first()


def list_sales_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SalesOrder).offset(skip).limit(limit).all()


def update_sales_order(db: Session, order_id: int, order_update: SalesOrderUpdate):
    db_order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not db_order:
        return None
    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_sales_order(db: Session, order_id: int):
    db_order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order


# ---- Sales Order Line CRUD ----
def add_sales_order_line(db: Session, order_id: int, line: SalesOrderLineCreate):
    db_line = SalesOrderLine(
        order_id=order_id,
        item_id=line.item_id,
        quantity=line.quantity,
        unit_price=line.unit_price,
        line_total=line.quantity * line.unit_price
    )
    db.add(db_line)

    # Update order total
    order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if order:
        order.total_amount += db_line.line_total

    db.commit()
    db.refresh(db_line)
    return db_line


def list_sales_order_lines(db: Session, order_id: int):
    return db.query(SalesOrderLine).filter(SalesOrderLine.order_id == order_id).all()
