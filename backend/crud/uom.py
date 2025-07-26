from sqlalchemy.orm import Session
from backend.models.uom import UnitOfMeasure
from backend.schemas.uom import UOMCreate, UOMConversionCreate
from backend.models.uom_conversion import UOMConversion
def create_uom(db: Session, uom: UOMCreate) -> UnitOfMeasure:
    new_uom = UnitOfMeasure(name=uom.name, symbol=uom.symbol)
    db.add(new_uom)
    db.commit()
    db.refresh(new_uom)
    return new_uom

def create_conversion(db: Session, conv: UOMConversionCreate) -> UOMConversion:
    new_conv = UOMConversion(
        base_uom_id=conv.base_uom_id,
        target_uom=conv.target_uom,
        factor=conv.factor
    )
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)
    return new_conv

def convert_quantity(db: Session, base_uom_id: int, target_symbol: str, quantity: float) -> float | None:
    """
    Converts a quantity from the base UOM to the target UOM using conversion factor.

    Example: If base_uom = "box", target_uom = "piece", and factor = 10,
    then convert_quantity(..., ..., ..., 2) returns 20.
    """
    conversion = db.query(UOMConversion).filter_by(
        base_uom_id=base_uom_id,
        target_uom=target_symbol
    ).first()

    if not conversion:
        return None

    return quantity * conversion.factor
#Convert by reverse
def convert_reverse_quantity(db: Session, target_symbol: str, base_uom_id: int, quantity: float) -> float | None:
    """
    Converts from target UOM back to base UOM (i.e., divides by factor).
    """
    conversion = db.query(UOMConversion).filter_by(
        base_uom_id=base_uom_id,
        target_uom=target_symbol
    ).first()

    if not conversion or conversion.factor == 0:
        return None

    return quantity / conversion.factor
#Verify that conversions exist
def conversion_exists(db: Session, base_uom_id: int, target_symbol: str) -> bool:
    return db.query(UOMConversion).filter_by(base_uom_id=base_uom_id, target_uom=target_symbol).first() is not None
