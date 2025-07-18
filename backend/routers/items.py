## inventory_bom_app/backend/routers/items.py
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
def create_item(item: dict, db: Session = Depends(get_db)):
    db_item = models.Item(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/")
def list_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()
