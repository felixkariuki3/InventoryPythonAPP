from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class BOM(Base):
    __tablename__ = "boms"

    id = Column(Integer, primary_key=True, index=True)
    parent_item_id = Column(Integer, ForeignKey("items.id"))
    component_item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer)

    parent_item = relationship("Item", foreign_keys=[parent_item_id], backref="bom_parents")
    component_item = relationship("Item", foreign_keys=[component_item_id], backref="bom_components")