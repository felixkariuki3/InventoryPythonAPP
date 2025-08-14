## inventory_bom_app/backend/routers/inventory.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.inventory import InventoryTransaction
from backend.models.item import Item
from utils.costing import calculate_weighted_average
from utils.costing import update_item_average_cost
from backend.schemas.stock_transaction import TransactionCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")

def create_transaction(txn: TransactionCreate, db: Session = Depends(get_db)):
    db_txn = InventoryTransaction(**txn)
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    

    if db_txn.transaction_type== "receipt":
        update_item_average_cost(
            db,
            item_id=db_txn.item_id,
            received_cost=db_txn.unit_cost,
            received_qty=db_txn.quantity,
            )
    return db_txn


@router.get("/")
def list_transactions(db: Session = Depends(get_db)):
    return db.query(InventoryTransaction).all()
