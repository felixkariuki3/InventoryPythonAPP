# services/items.py
from backend.models.item import Item

def get_item(db, item_id: int):
    """
    Retrieves an item by its ID.
    """
    return db.query(Item).filter(Item.item_id == item_id).first()
