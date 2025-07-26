## inventory_bom_app/backend/item.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    description = Column(String)
    quantity = Column(Integer)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    default_uom_id = Column(Integer, ForeignKey("uoms.id"),nullable = True)
    
    default_uom = relationship("UnitOfMeasure")

    warehouse = relationship("Warehouse", back_populates="items")
    
    conversions = relationship("UOMConversion", back_populates="item")
