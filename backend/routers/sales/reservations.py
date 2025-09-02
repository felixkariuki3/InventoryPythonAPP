from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.services.sales import reservations
from backend.schemas.sales.reservations import ReservationCreate, ReservationRead, ReservationUpdate

router = APIRouter(
    prefix="/sales/reservations",tags=["reservations"]
)


@router.post("/", response_model=ReservationRead)
def create_reservation(reservation_in: ReservationCreate, db: Session = Depends(get_db)):
    return reservations.ReservationService.create_reservation(db, reservation_in)

@router.put("/{reservation_id}", response_model=ReservationRead)
def update_reservation(reservation_id: int, reservation_in: ReservationUpdate, db: Session = Depends(get_db)):
    return reservations.ReservationService.update_reservation(db, reservation_id, reservation_in)

@router.post("/{reservation_id}/release", response_model=ReservationRead)
def release_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return reservations.ReservationService.release_reservation(db, reservation_id)

@router.get("/", response_model=List[ReservationRead])
def list_reservations(order_line_id: int = None, db: Session = Depends(get_db)):
    return reservations.ReservationService.list_reservations(db, order_line_id)