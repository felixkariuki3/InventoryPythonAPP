from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./inventory.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from backend.models import item, warehouse,bom,production_order,purchase,uom,uom_conversion,stock_transaction,inventory,wip
from backend.models.Sales import reservations,returns,invoices,sales_order,credit_notes,customers,adjustments,accounting,dnotes,payments