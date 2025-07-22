# backend/routers/production.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas import production_order as schemas
from backend.crud import production_order as crud
from backend.dependencies import get_db

router = APIRouter(prefix="/production", tags=["Production"])


@router.post("/", response_model=schemas.ProductionOrderResponse)
def create_order(order: schemas.ProductionOrderCreate, db: Session = Depends(get_db)):
    return crud.create_production_order(db, order)


@router.get("/", response_model=list[schemas.ProductionOrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)
