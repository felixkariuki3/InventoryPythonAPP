from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.schemas import bom as bom_schema
from backend.crud import bom as bom_crud

router = APIRouter(prefix="/boms", tags=["boms"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=bom_schema.BOMOut)
def create_bom(bom: bom_schema.BOMCreate, db: Session = Depends(get_db)):
    return bom_crud.create_bom(db, bom)

@router.get("/", response_model=list[bom_schema.BOMOut])
def read_boms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return bom_crud.get_boms(db, skip, limit)

@router.get("/{bom_id}", response_model=bom_schema.BOMOut)
def read_bom(bom_id: int, db: Session = Depends(get_db)):
    return bom_crud.get_bom(db, bom_id)