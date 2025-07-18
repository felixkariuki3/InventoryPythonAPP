## inventory_bom_app/backend/routers/items.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models
from backend.crud import item as item_crud
from backend.schemas import item as item_schema

router = APIRouter(prefix="/items", tags=["items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=item_schema.ItemOut)
def create(item: item_schema.ItemCreate, db: Session = Depends(get_db)):
    return item_crud.create_item(db, item)

@router.get("/", response_model=list[item_schema.ItemOut])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return item_crud.get_items(db, skip, limit)

@router.get("/{item_id}", response_model=item_schema.ItemOut)
def read_item(item_id: int, db: Session = Depends(get_db)):
    return item_crud.get_item(db, item_id)