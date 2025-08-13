# backend/models/wip.py
from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class WorkInProgress(Base):
    __tablename__ = "work_in_progress"

    id = Column(Integer, primary_key=True, index=True)
    production_order_id = Column(Integer, ForeignKey("production_orders.id",name="fk_work_in_progress_production_order_id"))
    item_id = Column(Integer, ForeignKey("items.item_id",name="fk_work_in_progress_item_id"), nullable=False)
    issued_quantity = Column(Float, default=0.0)
    cost_per_unit = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    completed_quantity = Column(Float, default=0.0)
    status = Column(String, default="in_progress")  # in_progress, completed, scrapped, paused
    updated_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("Item", back_populates="wips")
    production_order = relationship("ProductionOrder", back_populates="wip")
