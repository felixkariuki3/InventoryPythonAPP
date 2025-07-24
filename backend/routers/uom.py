from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.schemas.uom import UOMCreate, UOMConversionCreate, UOMOut, UOMConversionOut
from backend.crud import uom as uom_crud

router = APIRouter(prefix="/uom", tags=["UOM"])

@router.post("/", response_model=UOMOut)
def add_uom(uom: UOMCreate, db: Session = Depends(get_db)):
    return uom_crud.create_uom(db, uom)

@router.post("/conversion", response_model=UOMConversionOut)
def add_conversion(conv: UOMConversionCreate, db: Session = Depends(get_db)):
    return uom_crud.create_conversion(db, conv)
