# backend/models/wip.py
from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class WorkInProgress(Base):
    __tablename__ = "work_in_progress"

    id = Column(Integer, primary_key=True, index=True)
    production_order_id = Column(Integer, ForeignKey("production_orders.id"))
    issued_quantity = Column(Float, default=0.0)
    completed_quantity = Column(Float, default=0.0)
    status = Column(String, default="in_progress")  # in_progress, completed, scrapped, paused
    updated_at = Column(DateTime, default=datetime.utcnow)

    production_order = relationship("ProductionOrder", back_populates="wip")
