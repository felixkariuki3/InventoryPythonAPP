## inventory_bom_app/backend/main.py
from fastapi import FastAPI
from backend.database import engine, Base
from backend.routers import items, warehouses, bom, inventory

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manufacturing Inventory System")

# Include routers
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(warehouses.router, prefix="/warehouses", tags=["Warehouses"])
app.include_router(bom.router, prefix="/bom", tags=["Bill of Materials"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory Transactions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}