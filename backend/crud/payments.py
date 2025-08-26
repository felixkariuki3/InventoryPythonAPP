from sqlalchemy.orm import Session
from backend.models.sales import Payment
from backend.schemas.sales import PaymentCreate, PaymentUpdate

# ---- Payment CRUD ----
def create_payment(db: Session, payment: PaymentCreate):
    db_payment = Payment(
        customer_id=payment.customer_id,
        invoice_id=payment.invoice_id,
        payment_date=payment.payment_date,
        amount=payment.amount,
        method=payment.method,
        reference=payment.reference
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    # Optional: update invoice status if fully paid
    invoice = db_payment.invoice
    if invoice and db_payment.amount >= invoice.total_amount:
        invoice.status = "paid"
        db.commit()

    return db_payment


def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()


def list_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Payment).offset(skip).limit(limit).all()


def update_payment(db: Session, payment_id: int, payment_update: PaymentUpdate):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        return None
    for key, value in payment_update.dict(exclude_unset=True).items():
        setattr(db_payment, key, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def delete_payment(db: Session, payment_id: int):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if db_payment:
        db.delete(db_payment)
        db.commit()
    return db_payment
