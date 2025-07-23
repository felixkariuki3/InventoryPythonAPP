def convert_quantity(quantity: float, from_uom, to_uom):
    # If both UOMs have same base, convert via conversion factors
    if from_uom.base_unit_id == to_uom.base_unit_id or from_uom.id == to_uom.id:
        base_qty = quantity * from_uom.conversion_factor
        return base_qty / to_uom.conversion_factor
    raise ValueError("Incompatible UOMs: Cannot convert between unrelated units")
