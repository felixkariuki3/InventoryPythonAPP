## inventory_bom_app/backend/item.py
from sqlalchemy import REAL, TEXT, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Item(Base):
    __tablename__ = "items"

    name = Column(TEXT, unique=True, index=True)
    item_id =  Column(TEXT,primary_key=True, unique=True, index=True)
    description = Column(TEXT)
    quantity = Column(Integer)
    average_cost = Column(REAL, default=0.0)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id",name="fk_warehouses_id"),nullable=True)
    default_uom_id = Column(Integer, ForeignKey("uoms.id",name="fk_uoms_id"),nullable = True)
    
    default_uom = relationship("UnitOfMeasure")

    warehouse = relationship("Warehouse", back_populates="items")
    inventory = relationship("InventoryTransaction", back_populates="item")
    
    conversions = relationship("UOMConversion", back_populates="item")

    wips = relationship("WorkInProgress", back_populates="item")
    
    purchase_order_lines = relationship("PurchaseOrderLine", back_populates="item")
    
  
   
