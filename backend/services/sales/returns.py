from sqlalchemy.orm import Session
from backend.models.sales import SalesReturn
from backend.schemas.sales import SalesReturnCreate, SalesReturnUpdate

def create_return(db: Session, return_data: SalesReturnCreate):
    new_return = SalesReturn(**return_data.dict())
    db.add(new_return)
    db.commit()
    db.refresh(new_return)
    return new_return

def update_return(db: Session, return_id: int, return_data: SalesReturnUpdate):
    sales_return = db.query(SalesReturn).filter(SalesReturn.id == return_id).first()
    if not sales_return:
        return None
    for field, value in return_data.dict(exclude_unset=True).items():
        setattr(sales_return, field, value)
    db.commit()
    db.refresh(sales_return)
    return sales_return

def process_return(db: Session, return_id: int):
    sales_return = db.query(SalesReturn).filter(SalesReturn.id == return_id).first()
    if not sales_return or sales_return.status != "approved":
        return None
    
    # 1. Adjust inventory (increase stock back)
    # 2. Post financial adjustment (credit note or refund)
    
    sales_return.status = "completed"
    db.commit()
    db.refresh(sales_return)
    return sales_return
