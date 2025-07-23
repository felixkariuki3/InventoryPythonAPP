from backend.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class UnitOfMeasure(Base):
    __tablename__ = "units_of_measure"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)       # e.g., Kilogram
    symbol = Column(String, unique=True, nullable=False)     # e.g., kg
    base_unit_id = Column(Integer, ForeignKey("units_of_measure.id"), nullable=True)
    conversion_factor = Column(Float, default=1.0)  # relative to base unit

    base_unit = relationship("UnitOfMeasure", remote_side=[id], backref="derived_units")
