# backend/models/production.py
from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import relationship
from backend.database import Base
import enum
import datetime


class ProductionStatus(str, enum.Enum):
    planned = "Planned"
    in_progress = "In Progress"
    completed = "Completed"
    cancelled = "Cancelled"


class ProductionOrder(Base):
    __tablename__ = "production_orders"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id",name="fk_productions_orders_item_id"), nullable=False)
    quantity = Column(Float)
    status = Column(Enum(ProductionStatus), default=ProductionStatus.planned)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    item = relationship("Item")
    operations = relationship("ProductionOperation", back_populates="order", cascade="all, delete")
    wip = relationship("WorkInProgress", back_populates="production_order")


class ProductionOperation(Base):
    __tablename__ = "production_operations"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("production_orders.id",name="fk_productions_operations_order_id"), nullable=False)
    name = Column(String, nullable= False)
    sequence = Column(Integer)
    duration_minutes = Column(Float)

    order = relationship("ProductionOrder", back_populates="operations")
    