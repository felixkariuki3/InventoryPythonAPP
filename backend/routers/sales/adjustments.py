from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.schemas.sales.adjustments import SalesAdjustmentCreate, SalesAdjustmentRead, SalesAdjustmentUpdate
from backend.services.sales import adjustments

router = APIRouter(prefix="/sales/adjustments",tags=["Sales Adjustments"])

@router.post("/", response_model=SalesAdjustmentRead)
def create(adjustment: SalesAdjustmentCreate, db: Session = Depends(get_db)):
    return adjustments.create_adjustment(db, adjustment)

@router.get("/{adj_id}", response_model=SalesAdjustmentRead)
def get(adj_id: int, db: Session = Depends(get_db)):
    adj = adjustments.get_adjustment(db, adj_id)
    if not adj:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    return adj

@router.get("/", response_model=List[SalesAdjustmentRead])
def list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return adjustments.get_adjustments(db, skip, limit)

@router.put("/{adj_id}", response_model=SalesAdjustmentRead)
def update(adj_id: int, adjustment: SalesAdjustmentUpdate, db: Session = Depends(get_db)):
    adj = adjustments.update_adjustment(db, adj_id, adjustment)
    if not adj:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    return adj

@router.delete("/{adj_id}", response_model=SalesAdjustmentRead)
def delete(adj_id: int, db: Session = Depends(get_db)):
    adj = adjustments.delete_adjustment(db, adj_id)
    if not adj:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    return adj

