from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from backend.models.Sales.invoices import SalesInvoice
from backend.models.Sales.payments import Payment,PaymentAllocation
from backend.schemas.sales.payments import PaymentCreate,PaymentUpdate


def create_payment(db: Session, payment_in: PaymentCreate):
    # create base payment
    payment = Payment(
        customer_id=payment_in.customer_id,
        payment_date=payment_in.payment_date or datetime.utcnow(),
        method=payment_in.method,
        reference=payment_in.reference,
        amount=float(payment_in.amount),
        unallocated_amount=float(payment_in.amount),
        notes=payment_in.notes,
    )

    db.add(payment)
    db.flush()  # so payment.id is available

    # handle allocations
    for alloc_in in payment_in.allocations:
        # Check invoice exists
        invoice = db.query(SalesInvoice).filter(SalesInvoice.id == alloc_in.invoice_id).first()
        if not invoice:
            raise ValueError(f"Invoice {alloc_in.invoice_id} not found")

        # Create allocation
        allocation = PaymentAllocation(
            payment_id=payment.id,
            invoice_id=alloc_in.invoice_id,
            amount_applied=alloc_in.amount_applied,
        )
        db.add(allocation)

        # Reduce unallocated amount
        payment.unallocated_amount -= alloc_in.amount_applied

        # Reduce invoice balance
        invoice.balance -= alloc_in.amount_applied

    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()


def list_payments(db: Session, customer_id: Optional[int] = None):
    query = db.query(Payment)
    if customer_id:
        query = query.filter(Payment.customer_id == customer_id)
    return query.all()


def update_payment(db: Session, payment_id: int, payment_in: PaymentUpdate):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        return None

    for field, value in payment_in.dict(exclude_unset=True).items():
        setattr(payment, field, value)

    db.commit()
    db.refresh(payment)
    return payment


def delete_payment(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        return None
    db.delete(payment)
    db.commit()
    return payment

