from sqlalchemy.orm import Session
from backend.models.Sales.invoices import SalesInvoice, SalesInvoiceLine
from backend.schemas.sales.invoices import SalesInvoiceCreate, SalesInvoiceUpdate, SalesInvoiceLineCreate


# ---- Invoice CRUD ----
def create_invoice(db: Session, invoice: SalesInvoiceCreate):
    db_invoice = SalesInvoice(
        customer_id=invoice.customer_id,
        order_id=invoice.order_id,
        invoice_date=invoice.invoice_date,
        due_date=invoice.due_date,
        status=invoice.status or "unpaid",
        total_amount=0.0
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def get_invoice(db: Session, invoice_id: int):
    return db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()


def list_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SalesInvoice).offset(skip).limit(limit).all()


def update_invoice(db: Session, invoice_id: int, invoice_update: SalesInvoiceUpdate):
    db_invoice = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()
    if not db_invoice:
        return None
    for key, value in invoice_update.dict(exclude_unset=True).items():
        setattr(db_invoice, key, value)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def delete_invoice(db: Session, invoice_id: int):
    db_invoice = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()
    if db_invoice:
        db.delete(db_invoice)
        db.commit()
    return db_invoice


# ---- Invoice Line CRUD ----
def add_invoice_line(db: Session, invoice_id: int, line: SalesInvoiceLineCreate):
    db_line = SalesInvoiceLine(
        invoice_id=invoice_id,
        item_id=line.item_id,
        quantity=line.quantity,
        unit_price=line.unit_price,
        line_total=line.quantity * line.unit_price
    )
    db.add(db_line)

    # Update invoice total
    invoice = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id).first()
    if invoice:
        invoice.total_amount += db_line.line_total

    db.commit()
    db.refresh(db_line)
    return db_line


def list_invoice_lines(db: Session, invoice_id: int):
    return db.query(SalesInvoiceLine).filter(SalesInvoiceLine.invoice_id == invoice_id).all()
