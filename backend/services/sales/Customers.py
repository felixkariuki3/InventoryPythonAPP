from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.Sales.customers import Customer
from backend.schemas.sales.customers import CustomerCreate, CustomerUpdate


def create_customer(db: Session, customer_data: CustomerCreate):
    existing = db.query(Customer).filter(Customer.name == customer_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this name already exists")

    customer = Customer(**customer_data.dict())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customers(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Customer).offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def update_customer(db: Session, customer_id: int, update_data: CustomerUpdate):
    customer = get_customer(db, customer_id)
    for field, value in update_data.dict(exclude_unset=True).items():
        if value is not None: 
            setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int):
    customer = get_customer(db, customer_id)
    if customer.sales_orders:   # check relationship
        raise ValueError("Cannot delete customer with existing sales orders")
    db.delete(customer)
    db.commit()
    return {"detail": "Customer deleted"}
