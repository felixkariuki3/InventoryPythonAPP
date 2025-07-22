## inventory_bom_app/backend/main.py
from fastapi import FastAPI
from backend.database import engine, Base
from backend.routers import item
from backend.routers import warehouse
from backend.routers import bom
from backend.routers import stock_transaction
from backend.routers import production_order
from backend.routers import wip


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manufacturing Inventory System")

# Include routers
app.include_router(item.router)
app.include_router(warehouse.router)
app.include_router(bom.router)
app.include_router(stock_transaction.router)
app.include_router(production_order.router)
app.include_router(wip.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}