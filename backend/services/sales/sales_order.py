from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.sales import SalesOrder, SalesOrderLine, SalesOrderStatus
from backend.models.inventory import InventoryTransaction
from backend.models.sales import StockReservation
from backend.schemas.sales import SalesOrderCreate, SalesOrderUpdate
from backend.crud.sales_order import sales_orders


class SalesOrderService:

    @staticmethod
    def create_order(db: Session, order_in: SalesOrderCreate):
        order = sales_orders.create(db, obj_in=order_in)

        # Reserve stock for each line
        for line in order.lines:
            reservation = StockReservation(
                order_id=order.id,
                item_id=line.item_id,
                quantity=line.quantity,
                reserved_at=datetime.utcnow()
            )
            db.add(reservation)

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_order(db: Session, order_id: int, order_in: SalesOrderUpdate):
        order = sales_orders.update(db, db_obj=sales_orders.get(db, order_id), obj_in=order_in)
        return order

    @staticmethod
    def confirm_order(db: Session, order_id: int):
        order = sales_orders.get(db, order_id)
        if not order:
            raise ValueError("Order not found")
        order.status = SalesOrderStatus.CONFIRMED
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def fulfill_order(db: Session, order_id: int):
        order = sales_orders.get(db, order_id)
        if not order or order.status != SalesOrderStatus.CONFIRMED:
            raise ValueError("Order cannot be fulfilled")

        for line in order.lines:
            transaction = InventoryTransaction(
                item_id=line.item_id,
                quantity=-line.quantity,
                transaction_type="SALE",
                reference=f"SO-{order.id}"
            )
            db.add(transaction)

        order.status = SalesOrderStatus.FULFILLED
        db.commit()
        db.refresh(order)
        return order
