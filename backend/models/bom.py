from sqlalchemy import Column, Integer, ForeignKey,Float
from sqlalchemy.orm import relationship
from backend.database import Base

class BOM(Base):
    __tablename__ = "boms"

    id = Column(Integer, primary_key=True, index=True)
    parent_item_id = Column(Integer, ForeignKey("items.item_id", name="fk_items_item_id"))
    component_item_id = Column(Integer, ForeignKey("items.item_id", name="fk_Bomcomponent_item_id"))
    quantity = Column(Float)

    parent_item = relationship("Item", foreign_keys=[parent_item_id], backref="bom_parents")
    component_item = relationship("Item", foreign_keys=[component_item_id], backref="bom_components")