from sqlalchemy import (
    Column, Integer, Numeric, String, Float, DateTime, ForeignKey, Text, func
)
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


# ---------------------------
# Sales Returns
# ---------------------------
class SalesReturn(Base):
    __tablename__ = "sales_returns"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"))
    sales_order_line_id = Column(Integer, ForeignKey("sales_order_lines.id"), nullable=True)
    item_id = Column(Integer, ForeignKey("items.item_id"))
    quantity = Column(Float, nullable=False)
    reason = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, approved, rejected, completed
    created_at = Column(DateTime, default=datetime.utcnow)
