from sqlalchemy.orm import Session
from backend.models.Sales.sales_order import SalesOrder
from backend.models.Sales.payments import Payment
from backend.models.finance.accounting import JournalEntry,JournalLine




class SalesAccountingService:

    @staticmethod
    def post_invoice(db: Session, order_id: int):
        order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
        if not order:
            raise ValueError("Order not found")

        journal = JournalEntry(
            reference=f"SO-{order.id}",
            description="Sales Invoice",
        )
        db.add(journal)
        db.flush()

        # Debit Accounts Receivable
        db.add(JournalLine(
            journal_id=journal.id,
            account="AR",
            debit=order.total_amount
        ))

        # Credit Sales Revenue
        db.add(JournalLine(
            journal_id=journal.id,
            account="SALES",
            credit=order.total_amount
        ))

        db.commit()
        return journal

    @staticmethod
    def post_payment(db: Session, payment_id: int):
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise ValueError("Payment not found")

        journal = JournalEntry(
            reference=f"PAY-{payment.id}",
            description="Sales Payment"
        )
        db.add(journal)
        db.flush()

        # Debit Cash/Bank
        db.add(JournalLine(
            journal_id=journal.id,
            account="CASH",
            debit=payment.amount
        ))

        # Credit Accounts Receivable
        db.add(JournalLine(
            journal_id=journal.id,
            account="AR",
            credit=payment.amount
        ))

        db.commit()
        return journal
