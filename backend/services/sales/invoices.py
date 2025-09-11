from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from backend.models.Sales.invoices import SalesInvoice, SalesInvoiceLine
from backend.schemas.sales.invoices import (
    SalesInvoiceCreate, SalesInvoiceUpdate
)


def create_invoice(db: Session, invoice_in: SalesInvoiceCreate) -> SalesInvoice:
    """Create a sales invoice and its lines."""
    invoice = SalesInvoice(
        customer_id=invoice_in.customer_id,
        invoice_date=invoice_in.invoice_date or datetime.utcnow(),
        status=invoice_in.status or "DRAFT",
        total=invoice_in.total,
        balance=invoice_in.balance or invoice_in.total
    )
    db.add(invoice)
    db.flush()  # Get invoice ID

    for line in invoice_in.lines:
        db.add(SalesInvoiceLine(
            invoice_id=invoice.id,
            item_id=line.item_id,
            qty=line.qty,
            unit_price=line.unit_price,
            tax_rate=line.tax_rate or 0,
            discount_rate=line.discount_rate or 0
        ))

    db.commit()
    db.refresh(invoice)
    return invoice


def get_invoice(db: Session, invoice_id: int) -> Optional[SalesInvoice]:
    return db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()


def list_invoices(db: Session, customer_id: Optional[int] = None) -> List[SalesInvoice]:
    query = db.query(SalesInvoice)
    if customer_id:
        query = query.filter(SalesInvoice.customer_id == customer_id)
    return query.all()


def update_invoice(db: Session, invoice_id: int, invoice_update: SalesInvoiceUpdate) -> Optional[SalesInvoice]:
    invoice = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()
    if not invoice:
        return None
    
    for key, value in invoice_update.dict(exclude_unset=True).items():
        setattr(invoice, key, value)

    db.commit()
    db.refresh(invoice)
    return invoice


def delete_invoice(db: Session, invoice_id: int) -> bool:
    invoice = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()
    if not invoice:
        return False

    db.delete(invoice)
    db.commit()
    return True
