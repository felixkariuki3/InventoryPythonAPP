from sqlalchemy.orm import Session
from backend.models import warehouse as warehouse_model
from backend.schemas import warehouse as warehouse_schema

def create_warehouse(db: Session, warehouse: warehouse_schema.WarehouseCreate):
    db_warehouse = warehouse_model.Warehouse(**warehouse.dict())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

def get_warehouses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(warehouse_model.Warehouse).offset(skip).limit(limit).all()

def get_warehouse(db: Session, warehouse_id: int):
    return db.query(warehouse_model.Warehouse).filter(warehouse_model.Warehouse.id == warehouse_id).first()