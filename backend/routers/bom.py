## inventory_bom_app/backend/routers/bom.py
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
def create_bom(bom: dict, db: Session = Depends(get_db)):
    db_bom = models.BOM(**bom)
    db.add(db_bom)
    db.commit()
    db.refresh(db_bom)
    return db_bom

@router.get("/")
def list_bom(db: Session = Depends(get_db)):
    return db.query(models.BOM).all()