from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from backend.models.Sales.invoices import InvoiceStatus, SalesInvoice
from backend.models.Sales.payments import Payment, PaymentAllocation
from backend.schemas.sales.payments import PaymentCreate, PaymentUpdate


# ---------------------------
# Create Payment + Allocations
# ---------------------------
def create_payment(db: Session, payment_in: PaymentCreate):
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

    # Apply allocations
    for alloc_in in payment_in.allocations:
        invoice = db.query(SalesInvoice).filter(SalesInvoice.id == alloc_in.invoice_id).first()
        if not invoice:
            raise ValueError(f"Invoice {alloc_in.invoice_id} not found")

        if alloc_in.amount_applied > payment.unallocated_amount:
            raise ValueError("Allocation exceeds unallocated payment amount")

        if alloc_in.amount_applied > invoice.balance:
            raise ValueError(f"Allocation exceeds invoice {invoice.id} balance")

        allocation = PaymentAllocation(
            payment_id=payment.id,
            invoice_id=alloc_in.invoice_id,
            amount_applied=float(alloc_in.amount_applied),
        )
        db.add(allocation)

        # Reduce balances
        payment.unallocated_amount -= float(alloc_in.amount_applied)
        invoice.balance -= float(alloc_in.amount_applied)

        if invoice.balance <= 0:
            invoice.balance = 0
            invoice.status = InvoiceStatus.PAID
        elif invoice.balance < invoice.total:
            invoice.status = InvoiceStatus.PARTIAL
        else:
            invoice.status = InvoiceStatus.OPEN

    db.commit()
    db.refresh(payment)
    return payment


# ---------------------------
# Get Payment
# ---------------------------
def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()


# ---------------------------
# List Payments
# ---------------------------
def list_payments(db: Session, customer_id: Optional[int] = None):
    query = db.query(Payment)
    if customer_id:
        query = query.filter(Payment.customer_id == customer_id)
    return query.all()


# ---------------------------
# Update Payment
# ---------------------------
def update_payment(db: Session, payment_id: int, payment_in: PaymentUpdate):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        return None

    # Reverse old allocations
    for alloc in payment.allocations:
        invoice = db.query(SalesInvoice).filter(SalesInvoice.id == alloc.invoice_id).first()
        if invoice:
            invoice.balance += alloc.amount_applied
            invoice.status = "OPEN" if invoice.balance > 0 else invoice.status
        payment.unallocated_amount += alloc.amount_applied
    payment.allocations.clear()
    db.flush()

    # Update base fields (exclude allocations here!)
    base_data = payment_in.dict(exclude_unset=True, exclude={"allocations"})
    for field, value in base_data.items():
        if value is not None:
            setattr(payment, field, value)

    # Reapply allocations if provided
    if payment_in.allocations:
        for alloc_in in payment_in.allocations:
            invoice = db.query(SalesInvoice).filter(SalesInvoice.id == alloc_in.invoice_id).first()
            if not invoice:
                raise ValueError(f"Invoice {alloc_in.invoice_id} not found")

            if alloc_in.amount_applied > payment.unallocated_amount:
                raise ValueError("Allocation exceeds unallocated payment amount")

            if alloc_in.amount_applied > invoice.balance:
                raise ValueError(f"Allocation exceeds invoice {invoice.id} balance")

            allocation = PaymentAllocation(
                payment_id=payment.id,
                invoice_id=alloc_in.invoice_id,
                amount_applied=float(alloc_in.amount_applied),
            )
            db.add(allocation)

            payment.unallocated_amount -= float(alloc_in.amount_applied)
            invoice.balance -= float(alloc_in.amount_applied)
            if invoice.balance <= 0:
                invoice.balance = 0
                invoice.status = "PAID"

    db.commit()
    db.refresh(payment)
    return payment



# ---------------------------
# Delete Payment
# ---------------------------
def delete_payment(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        return None

    # Roll back allocations before deleting
    for alloc in payment.allocations:
        invoice = db.query(SalesInvoice).filter(SalesInvoice.id == alloc.invoice_id).first()
        if invoice:
           invoice.balance += alloc.amount_applied
        if invoice.balance >= invoice.total:
            invoice.status = InvoiceStatus.OPEN
        else:
            invoice.status = InvoiceStatus.PARTIAL

    db.delete(payment)
    db.commit()
    return payment
