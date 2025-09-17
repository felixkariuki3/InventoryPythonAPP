from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.dependencies import get_db
from backend.schemas.sales.invoices import SalesInvoiceRead, SalesInvoiceCreate
from backend.services.sales import invoices, accounting

router = APIRouter(prefix="/sales/invoices", tags=["Invoices"])


@router.post("/", response_model=SalesInvoiceRead)
def create_sales_invoice(invoice_in: SalesInvoiceCreate, db: Session = Depends(get_db)):
    return invoices.create_invoice(db, invoice_in)


@router.get("/", response_model=List[SalesInvoiceRead])
def list_sales_invoices(customer_id: int = None, db: Session = Depends(get_db)):
    return invoices.list_invoices(db, customer_id)


@router.get("/{invoice_id}", response_model=SalesInvoiceRead)
def get_sales_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = invoices.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/{order_id}/invoice", response_model=SalesInvoiceRead)
def generate_invoice_from_order(order_id: int, db: Session = Depends(get_db)):
    invoice = invoices.create_invoice_from_order(db, order_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Order not found")
    return invoice
