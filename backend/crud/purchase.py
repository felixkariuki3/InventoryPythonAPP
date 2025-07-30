from sqlalchemy.orm import Session
from backend.models.purchase import PurchaseOrder, PurchaseOrderItem
from schemas.purchase import PurchaseOrderCreate, PurchaseItemCreate

def create_purchase_order(db: Session, order_data: PurchaseOrderCreate):
    db_order = PurchaseOrder(
        supplier_id=order_data.supplier_id,
        order_date=order_data.order_date,
        status=order_data.status or "pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_purchase_order(db: Session, order_id: int):
    return db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()

def list_purchase_orders(db: Session):
    return db.query(PurchaseOrder).all()

def add_purchase_item(db: Session, order_id: int, item: PurchaseItemCreate):
    db_item = PurchaseOrderItem(
        purchase_order_id=order_id,
        item_id=item.item_id,
        quantity=item.quantity,
        unit_price=item.unit_price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def list_order_items(db: Session, order_id: int):
    return db.query(PurchaseOrderItem).filter(PurchaseOrderItem.purchase_order_id == order_id).all()
