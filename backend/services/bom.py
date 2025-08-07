# services/bom.py
from backend.models.bom import BOM
from sqlalchemy.orm import Session

def get_bom_for_item(db : Session, item_id: int):
    """
    Retrieves BOM components for a finished item.
    """
    return db.query(BOM).filter(BOM.parent_item_id == item_id).all()

