## inventory_bom_app/backend/item.py
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id",name="fk_inventory_transactions_item_id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id",name="fk_inventory_transactions_warehouse_id"))
    quantity = Column(Float)
    transaction_type = Column(String)  # e.g. receipt, issue, transfer
    reference = Column(String)
    unit_cost = Column(Float)

    item = relationship("Item")
    warehouse = relationship("Warehouse")
