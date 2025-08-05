# services/bom.py
from backend.models.bom import BOM

def get_bom_for_item(db, item_id: int):
    """
    Retrieves BOM components for a finished item.
    """
    return db.query(BOM).filter(BOM.parent_item_id == item_id).all()
