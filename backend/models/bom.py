## inventory_bom_app/backend/item.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class BOM(Base):
    __tablename__ = "bom"

    id = Column(Integer, primary_key=True, index=True)
    parent_item_id = Column(Integer, ForeignKey("items.id"))
    component_item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Float)