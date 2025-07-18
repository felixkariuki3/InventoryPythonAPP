## inventory_bom_app/backend/routers/warehouses.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_warehouse(warehouse: dict, db: Session = Depends(get_db)):
    db_warehouse = models.Warehouse(**warehouse)
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

@router.get("/")
def list_warehouses(db: Session = Depends(get_db)):
    return db.query(models.Warehouse).all()

