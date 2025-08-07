# services/inventory.py
from backend.models.item import Item
from backend.models.inventory import InventoryTransaction

def update_inventory_quantity(db, item_id: int, quantity_change: float):
    """
    Adjusts the quantity_on_hand for an item.
    """
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if item:
        Item.quantity = (Item.quantity or 0) + quantity_change

         # Log inventory transaction
        if type:
            log = InventoryTransaction(
                item_id=Item.id,
                quantity=quantity_change,
                transaction_type=type,
                reference="WIP Completed"
            )
            db.add(log)

        db.commit()
        db.refresh(item)
        return item
    return None
