from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.crud import warehouse as warehouse_crud
from backend.schemas import warehouse as warehouse_schema

router = APIRouter(prefix="/warehouses", tags=["warehouses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=warehouse_schema.Warehouse)
def create_warehouse(warehouse: warehouse_schema.WarehouseCreate, db: Session = Depends(get_db)):
    return warehouse_crud.create_warehouse(db, warehouse)

@router.get("/", response_model=list[warehouse_schema.Warehouse])
def read_warehouses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return warehouse_crud.get_warehouses(db, skip, limit)

@router.get("/{warehouse_id}", response_model=warehouse_schema.Warehouse)
def read_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    return warehouse_crud.get_warehouse(db, warehouse_id)