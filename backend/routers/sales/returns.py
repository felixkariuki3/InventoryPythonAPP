from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.schemas.sales.returns import SalesReturnCreate, SalesReturnResponse, SalesReturnUpdate
from backend.services.sales import returns

router = APIRouter(
    prefix="/sales/returns",tags=["Sales Returns"]
)

@router.post("/", response_model=SalesReturnResponse)
def create_sales_return(return_data: SalesReturnCreate, db: Session = Depends(get_db)):
    return returns.create_return(db, return_data)

@router.put("/{return_id}", response_model=SalesReturnResponse)
def update_sales_return(return_id: int, return_data: SalesReturnUpdate, db: Session = Depends(get_db)):
    updated = returns.update_return(db, return_id, return_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Return not found")
    return updated

@router.post("/{return_id}/process", response_model=SalesReturnResponse)
def process_sales_return(return_id: int, db: Session = Depends(get_db)):
    processed = returns.process_return(db, return_id)
    if not processed:
        raise HTTPException(status_code=400, detail="Return cannot be processed")
    return processed