from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from backend.schemas.sales.invoices import SalesInvoiceCreate
from backend.models.Sales.invoices import SalesInvoice, SalesInvoiceLine


def create_invoice(db: Session,invoice_in :SalesInvoiceCreate):
    invoice = SalesInvoice(
        customer_id =invoice_in.customer_id,
        invoice_date = invoice_in.invoice_date or datetime,
        status=invoice_in.status,
        total = invoice_in.total,
        balance = invoice_in.balance
    )
    db.add(invoice)
    db.flush()
    