from sqlalchemy.orm import Session
from backend.models.sales import StockReservation
from backend.schemas.sales import ReservationBase,ReservationCreate,ReservationRead,ReservationUpdate


class ReservationService:

    @staticmethod
    def create_reservation(db: Session, reservation_in: ReservationCreate):
        reservation = StockReservation(**reservation_in.dict())
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation

    @staticmethod
    def update_reservation(db: Session, reservation_id: int, reservation_in: ReservationUpdate):
        reservation = db.query(StockReservation).filter(StockReservation.id == reservation_id).first()
        if not reservation:
            return None
        for field, value in reservation_in.dict(exclude_unset=True).items():
            setattr(reservation, field, value)
        db.commit()
        db.refresh(reservation)
        return reservation

    @staticmethod
    def release_reservation(db: Session, reservation_id: int):
        reservation = db.query(StockReservation).filter(StockReservation.id == reservation_id).first()
        if reservation:
            reservation.status = "released"
            db.commit()
            db.refresh(reservation)
        return reservation

    @staticmethod
    def list_reservations(db: Session, order_line_id: int = None):
        query = db.query(StockReservation)
        if order_line_id:
            query = query.filter(StockReservation.sales_order_line_id == order_line_id)
        return query.all()
