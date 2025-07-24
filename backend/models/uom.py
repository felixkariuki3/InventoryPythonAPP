from sqlalchemy import Column, Integer, String
from backend.database import Base

class UnitOfMeasure(Base):
    __tablename__ = "uoms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False, unique=True)
