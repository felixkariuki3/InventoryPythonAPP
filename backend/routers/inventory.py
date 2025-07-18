## inventory_bom_app/backend/routers/inventory.py
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

def create_transaction(txn: dict, db: Session = Depends(get_db)):
    db_txn = models.InventoryTransaction(**txn)
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn

@router.get("/")
def list_transactions(db: Session = Depends(get_db)):
    return db.query(models.InventoryTransaction).all()
