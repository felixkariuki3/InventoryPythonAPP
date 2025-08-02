## inventory_bom_app/backend/item.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    quantity = Column(Float)
    transaction_type = Column(String)  # e.g. receipt, issue, transfer
    reference = Column(String)

    item = relationship("Item")
    warehouse = relationship("Warehouse")