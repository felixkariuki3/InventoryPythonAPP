from sqlalchemy.orm import Session
from backend.models.sales import SalesAdjustment, SalesOrder
from backend.schemas.sales import AdjustmentCreate
from backend.crud.sales_order import sales_adjustments


class AdjustmentService:

    @staticmethod
    def apply_adjustment(db: Session, adjustment_in: AdjustmentCreate):
        adjustment = sales_adjustments.create(db, obj_in=adjustment_in)

        order = db.query(SalesOrder).filter(SalesOrder.id == adjustment.order_id).first()
        if order:
            order.total_amount += adjustment.amount_change

        db.commit()
        db.refresh(adjustment)
        return adjustment
