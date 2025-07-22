# backend/routers/production_order.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.production_order import ProductionOrderCreate, ProductionOrderOut
from backend.crud import production_order as crud
from backend.database import get_db

router = APIRouter(prefix="/production_orders", tags=["Production Orders"])

@router.post("/", response_model=ProductionOrderOut)
def create_production_order(order: ProductionOrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@router.get("/", response_model=list[ProductionOrderOut])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_all_orders(db)
