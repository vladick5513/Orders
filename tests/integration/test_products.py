import pytest
from httpx import AsyncClient

async def test_create_product(async_client: AsyncClient):
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 100,
        "stock_quantity": 10
    }

    response = await async_client.post("/products/", json=product_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock_quantity"] == product_data["stock_quantity"]

async def test_read_product(async_client: AsyncClient, create_product_fixture):
    response = await async_client.get(f"/products/{create_product_fixture.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == create_product_fixture.id
    assert data["name"] == create_product_fixture.name
    assert data["description"] == create_product_fixture.description

async def test_update_product(async_client: AsyncClient, create_product_fixture):
    updated_product_data = {
        "name": "Updated Product",
        "description": "Updated product description",
        "price": 150,
        "stock_quantity": 20
    }

    response = await async_client.put(f"/products/{create_product_fixture.id}", json=updated_product_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == updated_product_data["name"]
    assert data["description"] == updated_product_data["description"]
    assert data["price"] == updated_product_data["price"]
    assert data["stock_quantity"] == updated_product_data["stock_quantity"]

async def test_delete_product(async_client: AsyncClient, create_product_fixture):
    response = await async_client.delete(f"/products/{create_product_fixture.id}")
    assert response.status_code == 200


    response = await async_client.get(f"/products/{create_product_fixture.id}")
    assert response.status_code == 404

async def test_read_products_by_price_range(async_client: AsyncClient, create_product_fixture):
    min_price = 50
    max_price = 200
    response = await async_client.get(f"/products/price_range/?min_price={min_price}&max_price={max_price}")
    assert response.status_code == 200

    data = response.json()
    assert any(min_price <= product["price"] <= max_price for product in data)

async def test_read_nonexistent_product(async_client: AsyncClient):
    response = await async_client.get("/products/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"