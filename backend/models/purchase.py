# backend/models/purchase.py
import enum
from sqlalchemy import Column, Enum, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class PurchaseOrderStatus(str, enum.Enum):
    OPEN = "open"
    PARTIALLY_RECEIVED = "partially_received"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(String, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(PurchaseOrderStatus), default=PurchaseOrderStatus.OPEN)

    lines = relationship("PurchaseOrderLine", back_populates="order", cascade="all, delete")


class PurchaseOrderLine(Base):
    __tablename__ = "purchase_order_lines"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("purchase_orders.id",name="fk_purchase_order_lines_order_id"))
    item_id = Column(Integer, ForeignKey("items.item_id",name="fk_purchase_order_lines_item_id"))
    quantity = Column(Float, nullable=False)
    received_qty = Column(Float, default=0)
    unit_cost = Column(Float, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id",name="fk_purchase_order_lines_warehouses_id"))
   

    order = relationship("PurchaseOrder", back_populates="lines")
    item = relationship("Item", back_populates="purchase_order_lines")



    
    
