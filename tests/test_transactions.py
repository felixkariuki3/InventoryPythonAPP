import pytest
from fastapi.testclient import TestClient
from main import app
from backend.database import SessionLocal, Base, engine
from backend.models.item import Item
from backend.models.warehouse import Warehouse
from backend.models.inventory import InventoryTransaction

client = TestClient(app)

# Use a separate test database or set up/teardown logic
@pytest.fixture(scope="module")
def setup_db():
    # Recreate all tables for a clean test environment
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Create test item and warehouse
    item = Item(item_id=1, name="Test Item", description="TESTSKU")
    warehouse = Warehouse(id=1, name="Test Warehouse")
    db.add_all([item, warehouse])
    db.commit()

    # Add initial inventory
    inv = InventoryTransaction(item_id=1, warehouse_id=1, quantity=10.0)
    db.add(inv)
    db.commit()
    db.close()
    yield
    # Teardown is optional here


def test_issue_transaction(setup_db):
    payload = {
        "item_id": 1,
        "warehouse_id": 1,
        "quantity": 2.0
    }
    response = client.post("/transactions/issue", json=payload)
    assert response.status_code == 200
   
    logs = response.json()
    print ("RESPONSE JSON:",logs)
    if isinstance(logs, dict):
        logs = logs.get("logs") or logs.get("data") or [logs]  # fallback

    # Ensure it's a list before looping
    assert isinstance(logs, list), f"Expected list, got {type(logs)}"

    assert any(
        log["item_id"] == 1 and
        log["warehouse_id"] == 1 and
        log["change"] == -2.0 and
        log["note"] == "issue"
        for log in logs
    )


def test_insufficient_stock(setup_db):
    payload = {
        "item_id": 1,
        "warehouse_id": 1,
        "quantity": 100.0  # More than available
    }
    response = client.post("/transactions/issue", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stock"

