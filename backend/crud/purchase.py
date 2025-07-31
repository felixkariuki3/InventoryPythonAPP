from sqlalchemy.orm import Session
from backend.models.purchase import PurchaseOrder, PurchaseOrderLine
from backend.schemas.purchase import PurchaseOrderCreate, PurchaseOrderLineCreate
from backend.models.stock_transaction import InventoryLog


def create_purchase_order(db: Session, order_data: PurchaseOrderCreate):
    db_order = PurchaseOrder(
        supplier_id=order_data.supplier_id,
        order_date=order_data.order_date,
        status=order_data.status or "pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for line in order_data.lines:
        db_line = PurchaseOrderLine(
            order_id=db_order.id,
            item_id=line.item_id,
            quantity=line.quantity,
            unit_cost=line.unit_cost
        )
        db.add(db_line)

    db.commit()
    db.refresh(db_order)
    return db_order

def get_purchase_order(db: Session, order_id: int):
    return db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()

def list_purchase_orders(db: Session):
    return db.query(PurchaseOrder).all()

def add_purchase_item(db: Session, order_id: int, item: PurchaseOrderLineCreate):
    db_item = PurchaseOrderLineCreate(
        purchase_order_id=order_id,
        item_id=item.item_id,
        quantity=item.quantity,
        unit_price=item.unit_price
    )
    db.add(db_item)
    InventoryLog(
        db=db,
        item_id=item.id,
        warehouse_id=item.warehouse_id,  # Replace with actual warehouse if tracked
        quantity=PurchaseOrderLine.quantity,
        note=f"PO #{order_id} created"
        )
    db.commit()
    db.refresh(db_item)
    return db_item

def list_order_items(db: Session, order_id: int):
    return db.query(PurchaseOrderLineCreate).filter(PurchaseOrderLineCreate.purchase_order_id == order_id).all()
