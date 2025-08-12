from sqlalchemy import Column, Integer, Float, ForeignKey
from backend.database import Base
from sqlalchemy.orm import relationship

class UOMConversion(Base):
    __tablename__ = "uom_conversions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id",name="fk_uom_conversions_item_id"))
    base_uom_id = Column(Integer, ForeignKey("uoms.id",name="fk_uom_conversions_base_uom_id"))
    target_uom = Column(Integer, ForeignKey("uoms.id",name="fk_uom_conversions_target_uom_id"))
    factor = Column(Float, nullable=False)

    item = relationship("Item", back_populates="conversions")
    from_uom = relationship("UnitOfMeasure", foreign_keys=[base_uom_id])
    to_uom = relationship("UnitOfMeasure", foreign_keys=[target_uom])
