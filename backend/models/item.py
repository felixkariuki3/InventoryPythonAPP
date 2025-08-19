## inventory_bom_app/backend/item.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Item(Base):
    __tablename__ = "items"

    name = Column(String, unique=True, index=True)
    item_id =  Column(String,primary_key=True, unique=True, index=True)
    description = Column(String)
    quantity = Column(Integer)
    average_cost = Column(Float, default=0.0)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id",name="fk_warehouses_id"),nullable=True)
    default_uom_id = Column(Integer, ForeignKey("uoms.id",name="fk_uoms_id"),nullable = True)
    
    default_uom = relationship("UnitOfMeasure")

    warehouse = relationship("Warehouse", back_populates="items")
    
    conversions = relationship("UOMConversion", back_populates="item")

    wips = relationship("WorkInProgress", back_populates="item")
    
  
   
