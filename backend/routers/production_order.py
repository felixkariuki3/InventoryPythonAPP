# backend/routers/production.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas import production_order as schemas
from backend.crud import production_order as crud
from backend.dependencies import get_db
from backend.services import production_service
from backend.schemas.production_order import ProductionStartRequest, ProductionCompleteRequest, ProductionOrderIssue
from backend.models.wip import WorkInProgress
from backend.schemas.wip import WIPEntry

router = APIRouter(prefix="/production", tags=["Production"])


@router.post("/", response_model=schemas.ProductionOrderResponse)
def create_order(order: schemas.ProductionOrderCreate, db: Session = Depends(get_db)):
    return crud.create_production_order(db, order)


@router.get("/", response_model=list[schemas.ProductionOrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@router.post("/start")
def start_order(data: ProductionStartRequest, db: Session = Depends(get_db)):
    production_service.start_production_order(db, data.order_id)
    return {"message": "Production started"}

@router.post("/issue")
def issue_materials(data: ProductionOrderIssue, db: Session = Depends(get_db)):
    production_service.issue_materials_for_production(db, data.order_id)
    return {"message": "Materials for {data.item_id}Issued"}

@router.post("/complete")
def complete_order(data: ProductionCompleteRequest, db: Session = Depends(get_db)):
    production_service.complete_production_order(db, data.order_id, data.completed_quantity)
    return {"message": "Production completed"}
# routers/production.py

@router.get("/production/{order_id}/wip", response_model=List[WIPEntry])
def get_wip_for_production_order(order_id: int, db: Session = Depends(get_db)):
    wip_entries = db.query(WorkInProgress).filter(WorkInProgress.production_order_id == order_id).all()
    return wip_entries
