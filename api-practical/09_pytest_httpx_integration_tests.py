from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel
import pytest
from httpx import AsyncClient, ASGITransport

app = FastAPI(
    title="Integration Testing API",
    version="1.0.0"
)

class Item(BaseModel):
    id: int
    name: str
    price: float

items_db = {
    1: {"id": 1, "name": "Data Science Textbook", "price": 49.99},
    2: {"id": 2, "name": "Python Cheatsheet", "price": 9.99}
}

@app.get("/")
def root():
    return {"message": "API for Testing"}

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return items_db[item_id]

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    items_db[item.id] = item.model_dump()
    return item

client = TestClient(app)

def test_read_root_sync():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API for Testing"}

def test_read_item_not_found_sync():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item Not Found"

@pytest.mark.asyncio
async def test_read_item_success_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Data Science Textbook"

@pytest.mark.asyncio
async def test_create_item_success_async():
    transport = ASGITransport(app=app)
    new_item_payload = {"id": 3, "name": "FastAPI Guide", "price": 29.99}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items", json=new_item_payload)
    assert response.status_code == 201
    assert response.json() == new_item_payload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
