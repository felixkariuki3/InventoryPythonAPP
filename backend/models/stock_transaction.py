from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, ForeignKey, DateTime,VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id",name="fk_transactions_item_id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id",name="fk_transactions_warehouse_id"))
    type = Column(String)  # 'receipt', 'issue', 'transfer', 'adjustment'
    quantity = Column(Float)
    unit_cost = Column(Float)
    reference = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    item = relationship("Item")
    warehouse = relationship("Warehouse")

class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", name="fk_inventory_logs_warehouse_id"))
    transaction_id = Column(VARCHAR, ForeignKey("transactions.id",name="fk_inventory_logs_transaction_id"))
    change = Column(Float)  # +ve or -ve quantity
    note = Column(String)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)

    item = relationship("Item")
    warehouse = relationship("Warehouse")
    transaction = relationship("Transaction")