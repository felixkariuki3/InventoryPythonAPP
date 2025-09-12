from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class DeliveryNote(Base):
    __tablename__ = "delivery_notes"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id", name="fk_dn_sales_order_id"))
    delivery_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, default="DRAFT", index=True)  # DRAFT, SHIPPED, CANCELLED
    reference = Column(String)

    sales_order = relationship("SalesOrder", back_populates="delivery_notes")
    lines = relationship(
        "DeliveryNoteLine",
        back_populates="delivery_note",
        cascade="all, delete-orphan"
    )


class DeliveryNoteLine(Base):
    __tablename__ = "delivery_note_lines"

    id = Column(Integer, primary_key=True, index=True)
    delivery_note_id = Column(
        Integer,
        ForeignKey("delivery_notes.id", name="fk_dnl_delivery_note_id"),
        nullable=False,
        index=True
    )
    order_line_id = Column(Integer, ForeignKey("sales_order_lines.id", name="fk_dnl_order_line_id"))
    item_id = Column(String, ForeignKey("items.item_id", name="fk_dnl_item_id"), nullable=False, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", name="fk_dnl_warehouse_id"))
    qty_shipped = Column(Float, nullable=False)
    unit_cost = Column(Float)

    delivery_note = relationship("DeliveryNote", back_populates="lines")
    order_line = relationship("SalesOrderLine")
    warehouse = relationship("Warehouse")
