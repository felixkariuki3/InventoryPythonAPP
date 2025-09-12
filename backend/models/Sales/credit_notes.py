from sqlalchemy import (
    Column, Integer, Numeric, String, DateTime, ForeignKey, Text, Float
)
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class CreditNote(Base):
    __tablename__ = "credit_notes"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", name="fk_cn_customer_id"), nullable=False, index=True)
    credit_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, default="DRAFT", index=True)  # DRAFT, POSTED, APPLIED, CANCELLED
    reference_invoice_id = Column(Integer, ForeignKey("sales_invoices.id", name="fk_cn_reference_invoice_id"))
    subtotal = Column(Float, default=0, nullable=False)
    tax_total = Column(Float, default=0, nullable=False)
    total = Column(Float, default=0, nullable=False)
    notes = Column(Text)

    customer = relationship("Customer", back_populates="credit_notes")
    reference_invoice = relationship("SalesInvoice", backref="credit_notes")
    lines = relationship(
        "CreditNoteLine",
        back_populates="credit_note",
        cascade="all, delete-orphan"
    )


class CreditNoteLine(Base):
    __tablename__ = "credit_note_lines"

    id = Column(Integer, primary_key=True, index=True)
    credit_note_id = Column(
        Integer,
        ForeignKey("credit_notes.id", name="fk_cnl_credit_note_id"),
        nullable=False,
        index=True
    )
    item_id = Column(String, ForeignKey("items.item_id", name="fk_cnl_item_id"), nullable=False, index=True)
    qty = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0)
    reason = Column(String)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", name="fk_cnl_warehouse_id"))

    credit_note = relationship("CreditNote", back_populates="lines")
    warehouse = relationship("Warehouse")
