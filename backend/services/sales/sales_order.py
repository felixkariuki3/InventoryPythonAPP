from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.Sales.sales_order import SalesOrder, SalesOrderLine, SalesOrderStatus
from backend.models.inventory import InventoryTransaction
from backend.models.Sales.reservations import StockReservation
from backend.schemas.sales.sales_order import (
    SalesOrderCreate,
    SalesOrderUpdate,
    SalesOrderLineCreate
)


class SalesOrderService:

    # ---------------------------
    # SALES ORDER CRUD
    # ---------------------------

    @staticmethod
    def create_order(db: Session, order_in: SalesOrderCreate):
        """Create a sales order with lines and reserve stock."""
        order = SalesOrder(
            customer_id=order_in.customer_id,
            order_date=order_in.order_date,
            due_date=order_in.due_date,
            status=order_in.status or SalesOrderStatus.DRAFT,
            total_amount=0.0
        )
        db.add(order)
        db.flush()  # Get order.id before adding lines

        total_amount = 0
        for line_in in order_in.lines:
            line_total = line_in.ordered_qty * line_in.unit_price
            total_amount += line_total

            line = SalesOrderLine(
                order_id=order.id,
                item_id=line_in.item_id,
                ordered_qty=line_in.ordered_qty,
                unit_price=line_in.unit_price,
                line_total=line_total,
                warehouse_id=line_in.warehouse_id
            )
            db.add(line)
            db.flush()

            # Reserve stock
            reservation = StockReservation(
                sales_order_line_id=line.id,
                item_id=line_in.item_id,
                reserved_qty=line_in.ordered_qty,
                created_at=datetime.utcnow(),
                warehouse_id=line_in.warehouse_id
            )
            db.add(reservation)

        order.total_amount = total_amount
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_order(db: Session, order_id: int):
        return db.query(SalesOrder).filter(SalesOrder.id == order_id).first()

    @staticmethod
    def list_orders(db: Session, skip: int = 0, limit: int = 100):
        return db.query(SalesOrder).offset(skip).limit(limit).all()

    @staticmethod
    def update_order(db: Session, order_id: int, order_in: SalesOrderUpdate):
        order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
        if not order:
            return None

    # update scalar fields only
        data = order_in.dict(exclude_unset=True, exclude={"lines", "reservations"})
        for key, value in data.items():
            if value is not None: 
                setattr(order, key, value)

    # handle lines if provided
        if order_in.lines is not None:
            order.lines.clear()
        for line_data in order_in.lines:
            line = SalesOrderLine(**line_data.dict())
            order.lines.append(line)

    # handle reservations if provided
        if order_in.reservations is not None and len(order_in.reservations) > 0:
            order.reservations.clear()
        for res_data in order_in.reservations:
            reservation = StockReservation(**res_data.dict())
            order.reservations.append(reservation)

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def delete_order(db: Session, order_id: int):
        order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
        if order:
            db.delete(order)
            db.commit()
        return order

    # ---------------------------
    # SALES ORDER LINES
    # ---------------------------

    @staticmethod
    def add_order_line(db: Session, order_id: int, line_in: SalesOrderLineCreate):
        """Add a line to a sales order and update totals."""
        order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
        if not order:
            raise ValueError("Order not found")

        line_total = line_in.ordered_qty * line_in.unit_price
        line = SalesOrderLine(
            order_id=order.id,
            item_id=line_in.item_id,
            ordered_qty=line_in.ordered_qty,
            unit_price=line_in.unit_price,
            line_total=line_total,
            warehouse_id=line_in.warehouse_id
        )
        db.add(line)

        # Reserve stock
        reservation = StockReservation(
            order_id=order.id,
            item_id=line_in.item_id,
            quantity=line_in.ordered_qty,
            reserved_at=datetime.utcnow()
        )
        db.add(reservation)

        # Update total
        order.total_amount += line_total
        db.commit()
        db.refresh(line)
        return line

    @staticmethod
    def list_order_lines(db: Session, order_id: int):
        return db.query(SalesOrderLine).filter(SalesOrderLine.order_id == order_id).all()

    # ---------------------------
    # BUSINESS LOGIC
    # ---------------------------

    @staticmethod
    def confirm_order(db: Session, order_id: int):
        order = SalesOrderService.get_order(db, order_id)
        if not order:
            raise ValueError("Order not found")
        order.status = SalesOrderStatus.CONFIRMED
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def fulfill_order(db: Session, order_id: int):
        order = SalesOrderService.get_order(db, order_id)
        if not order or order.status != SalesOrderStatus.CONFIRMED:
            raise ValueError("Order cannot be fulfilled")

        for line in order.lines:
            transaction = InventoryTransaction(
                item_id=line.item_id,
                quantity=-line.ordered_quantity,
                transaction_type="SALE",
                reference=f"SO-{order.id}"
            )
            db.add(transaction)

        order.status = SalesOrderStatus.FULFILLED
        db.commit()
        db.refresh(order)
        return order
