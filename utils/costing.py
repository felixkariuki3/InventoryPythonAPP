from backend.models.item import Item
from sqlalchemy.orm import Session

#Calculating the Weighted average cost
def calculate_weighted_average(current_qty: float, current_cost: float, new_qty: float, new_cost: float) -> float:
    total_cost = (current_qty * current_cost) + (new_qty * new_cost)
    total_qty = current_qty + new_qty
    if total_qty == 0:
        return 0.0
    return total_cost / total_qty

#Updating the item average cost after the receipting transaction
def update_item_average_cost(db: Session, item_id: int, received_qty: float, received_cost: float):
    item = db.query(Item).filter(Item.item_id == item_id).first()

    if item:
        current_qty = item.quantity or 0
        current_cost = item.average_cost or 0.0

        new_avg_cost = calculate_weighted_average(current_qty, current_cost, received_qty, received_cost)
        item.average_cost = new_avg_cost

        db.add(item)
        db.commit()
        db.refresh(item)