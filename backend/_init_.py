from backend.database import Base, engine
from backend.models import item, warehouse, inventory, bom

Base.metadata.create_all(bind=engine)