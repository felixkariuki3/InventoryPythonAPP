def calculate_weighted_average(current_qty: float, current_cost: float, new_qty: float, new_cost: float) -> float:
    total_cost = (current_qty * current_cost) + (new_qty * new_cost)
    total_qty = current_qty + new_qty
    if total_qty == 0:
        return 0.0
    return total_cost / total_qty
