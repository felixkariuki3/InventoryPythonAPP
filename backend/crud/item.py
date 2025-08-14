from sqlalchemy.orm import Session
from backend.models import item as item_model
from backend.schemas import item as item_schema

def create_item(db: Session, item: item_schema.ItemCreate):
    db_item = item_model.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(item_model.Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(item_model.Item).filter(item_model.Item.item_id == item_id).first()
