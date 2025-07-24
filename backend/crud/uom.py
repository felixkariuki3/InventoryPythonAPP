from sqlalchemy.orm import Session
from backend.models.uom import UnitOfMeasure, UOMConversion
from backend.schemas.uom import UOMCreate, UOMConversionCreate

def create_uom(db: Session, uom: UOMCreate):
    new_uom = UnitOfMeasure(name=uom.name, symbol=uom.symbol)
    db.add(new_uom)
    db.commit()
    db.refresh(new_uom)
    return new_uom

def create_conversion(db: Session, conv: UOMConversionCreate):
    new_conv = UOMConversion(
        base_uom_id=conv.base_uom_id,
        target_uom=conv.target_uom,
        factor=conv.factor
    )
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)
    return new_conv

def convert_quantity(db: Session, base_uom_id: int, target_symbol: str, quantity: float):
    conversion = db.query(UOMConversion).filter_by(base_uom_id=base_uom_id, target_uom=target_symbol).first()
    if not conversion:
        return None
    return quantity * conversion.factor
