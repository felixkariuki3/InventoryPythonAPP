from sqlalchemy.orm import Session
from backend.models.sales import StockReservation
from backend.schemas.sales import ReservationCreate
from backend.crud.sales_order import stock_reservations


class ReservationService:

    @staticmethod
    def create_reservation(db: Session, reservation_in: ReservationCreate):
        reservation = stock_reservations.create(db, obj_in=reservation_in)
        db.commit()
        db.refresh(reservation)
        return reservation

    @staticmethod
    def release_reservation(db: Session, reservation_id: int):
        reservation = stock_reservations.get(db, reservation_id)
        if reservation:
            db.delete(reservation)
            db.commit()
        return True
