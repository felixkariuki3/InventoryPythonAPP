from sqlalchemy.orm import Session
from backend.models.Sales.sales_order import SalesAdjustment, SalesOrder
from backend.schemas.sales import SalesAdjustmentCreate,SalesAdjustmentRead,SalesAdjustmentUpdate,SalesAdjustmentBase



def create_adjustment(db: Session, adjustment: SalesAdjustmentCreate):
    db_adj = SalesAdjustment(**adjustment.dict())
    db.add(db_adj)
    db.commit()
    db.refresh(db_adj)
    return db_adj

# Get by ID
def get_adjustment(db: Session, adj_id: int):
    return db.query(SalesAdjustment).filter(SalesAdjustment.id == adj_id).first()

# List
def get_adjustments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SalesAdjustment).offset(skip).limit(limit).all()

# Update
def update_adjustment(db: Session, adj_id: int, adjustment: SalesAdjustmentUpdate):
    db_adj = db.query(SalesAdjustment).filter(SalesAdjustment.id == adj_id).first()
    if not db_adj:
        return None
    for field, value in adjustment.dict(exclude_unset=True).items():
        setattr(db_adj, field, value)
    db.commit()
    db.refresh(db_adj)
    return db_adj

# Delete
def delete_adjustment(db: Session, adj_id: int):
    db_adj = db.query(SalesAdjustment).filter(SalesAdjustment.id == adj_id).first()
    if db_adj:
        db.delete(db_adj)
        db.commit()
    return db_adj