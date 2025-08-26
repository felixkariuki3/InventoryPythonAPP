from sqlalchemy.orm import Session
from backend.models.sales import SalesReturn, SalesOrder, SalesOrderStatus
from backend.models.inventory import InventoryTransaction
from backend.schemas.sales import ReturnCreate
from backend.crud.sales_order import sales_returns


class ReturnService:

    @staticmethod
    def process_return(db: Session, return_in: ReturnCreate):
        sales_return = sales_returns.create(db, obj_in=return_in)

        # Add back stock
        for line in sales_return.lines:
            transaction = InventoryTransaction(
                item_id=line.item_id,
                quantity=line.quantity,
                transaction_type="RETURN",
                reference=f"SR-{sales_return.id}"
            )
            db.add(transaction)

        # Optionally mark order as partially returned
        order = db.query(SalesOrder).filter(SalesOrder.id == sales_return.order_id).first()
        if order:
            order.status = SalesOrderStatus.RETURNED

        db.commit()
        db.refresh(sales_return)
        return sales_return
