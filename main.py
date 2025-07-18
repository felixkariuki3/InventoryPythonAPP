## inventory_bom_app/backend/main.py
from fastapi import FastAPI
from backend.database import engine, Base
from backend.routers import item


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manufacturing Inventory System")

# Include routers
app.include_router(item.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}