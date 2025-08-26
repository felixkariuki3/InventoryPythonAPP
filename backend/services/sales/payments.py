from sqlalchemy.orm import Session
from backend.models.sales import SalesPayment, SalesOrder, SalesOrderStatus
from backend.schemas.sales import PaymentCreate
from backend.crud.sales_order import sales_payments


class PaymentService:

    @staticmethod
    def record_payment(db: Session, payment_in: PaymentCreate):
        payment = sales_payments.create(db, obj_in=payment_in)

        order = db.query(SalesOrder).filter(SalesOrder.id == payment.order_id).first()
        if order:
            if payment.amount >= order.total_amount:
                order.status = SalesOrderStatus.PAID

        db.commit()
        db.refresh(payment)
        return payment
