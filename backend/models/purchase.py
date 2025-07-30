# backend/models/purchase.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(String, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="open")  # open, received, cancelled

    lines = relationship("PurchaseOrderLine", back_populates="order", cascade="all, delete")


class PurchaseOrderLine(Base):
    __tablename__ = "purchase_order_lines"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("purchase_orders.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Float, nullable=False)
    unit_cost = Column(Float, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))

    order = relationship("PurchaseOrder", back_populates="lines")
