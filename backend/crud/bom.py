from sqlalchemy.orm import Session
from backend.models import bom as bom_model
from backend.schemas import bom as bom_schema

def create_bom(db: Session, bom: bom_schema.BOMCreate):
    db_bom = bom_model.BOM(**bom.dict())
    db.add(db_bom)
    db.commit()
    db.refresh(db_bom)
    return db_bom

def get_boms(db: Session, skip: int = 0, limit: int = 10):
    return db.query(bom_model.BOM).offset(skip).limit(limit).all()

def get_bom(db: Session, bom_id: int):
    return db.query(bom_model.BOM).filter(bom_model.BOM.id == bom_id).first()