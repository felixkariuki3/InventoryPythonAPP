## inventory_bom_app/backend/main.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base
from backend.routers import item
from backend.routers import warehouse
from backend.routers import bom
from backend.routers import stock_transaction
from backend.routers import production_order
from backend.routers import wip
from backend.routers import uom
from backend.routers import purchase



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manufacturing Inventory System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(item.router)
app.include_router(warehouse.router)
app.include_router(bom.router)
app.include_router(stock_transaction.router)
app.include_router(production_order.router)
app.include_router(wip.router)
app.include_router(uom.router)
app.include_router(purchase.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")