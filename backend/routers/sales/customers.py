from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.dependencies import get_db
from backend.schemas.sales.customers import CustomerCreate, CustomerUpdate, CustomerRead
from backend.services.sales import Customers as service

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerRead)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return service.create_customer(db, customer)


@router.get("/", response_model=List[CustomerRead])
def list_customers(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return service.get_customers(db, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return service.get_customer(db, customer_id)


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    return service.update_customer(db, customer_id, customer)


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return service.delete_customer(db, customer_id)
