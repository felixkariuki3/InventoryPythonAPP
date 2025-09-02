from sqlalchemy import (
    Column, Integer, Numeric, String, Float, DateTime, ForeignKey, Text, func
)
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class StockReservation(Base):
    __tablename__ = "stock_reservations"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_line_id = Column(Integer, ForeignKey("sales_order_lines.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    reserved_qty = Column(Float, nullable=False)
    released_qty = Column(Float, default=0)
    status = Column(String, default="active")  # active, fulfilled, cancelled
    created_at = Column(DateTime, default=func.now())

    # relations
    order_line = relationship("SalesOrderLine", back_populates="reservations")
    item = relationship("Item")
    warehouse = relationship("Warehouse")
    order_line = relationship("SalesOrderLine", back_populates="reservations")