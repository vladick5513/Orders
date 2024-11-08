import pytest
from httpx import AsyncClient


async def test_create_order_items(async_client: AsyncClient, create_customer_fixture, create_order_fixture, create_product_fixture):
    order_items_data = {
        "order_id": create_order_fixture.id,
        "product_id": create_product_fixture.id,
        "quantity": 2,
        "price": 100.0,
        "total_price": 200.0
    }
    responses = await async_client.post("/order_items/", json=order_items_data)
    assert responses.status_code == 200
    data = responses.json()
    assert data["order_id"] == create_order_fixture.id
    assert data["product_id"] == create_product_fixture.id
    assert data["quantity"] == order_items_data["quantity"]
    assert data["total_price"] == order_items_data["total_price"]

async def test_read_order_item(async_client: AsyncClient, create_order_item_fixture):
    response = await async_client.get(f"/order_items/{create_order_item_fixture['id']}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == create_order_item_fixture["id"]
    assert data["order_id"] == create_order_item_fixture["order_id"]
    assert data["product_id"] == create_order_item_fixture["product_id"]
    assert data["quantity"] == create_order_item_fixture["quantity"]

async def test_update_order_item(async_client: AsyncClient, create_order_item_fixture):
    updated_order_item_data = {
        "order_id": create_order_item_fixture["order_id"],
        "product_id": create_order_item_fixture["product_id"],
        "quantity": 3,
        "price": 100.0,
        "total_price": 300.0
    }
    response = await async_client.put(f"/order_items/{create_order_item_fixture['id']}", json=updated_order_item_data)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == create_order_item_fixture["id"]
    assert data["order_id"] == create_order_item_fixture["order_id"]
    assert data["product_id"] == create_order_item_fixture["product_id"]
    assert data["quantity"] == updated_order_item_data["quantity"]
    assert data["total_price"] == updated_order_item_data["total_price"]


async def test_delete_order_item(async_client: AsyncClient, create_order_item_fixture):
    response = await async_client.delete(f"/order_items/{create_order_item_fixture['id']}")
    assert response.status_code == 200

    response = await async_client.get(f"/order_items/{create_order_item_fixture['id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "OrderItem not found"


async def test_read_order_items_by_price_range(async_client: AsyncClient, create_order_item_fixture):
    min_price = 50.0
    max_price = 250.0
    response = await async_client.get(f"/order_items/price_range?min_price={min_price}&max_price={max_price}")
    assert response.status_code == 200

    data = response.json()
    assert any(min_price <= item["price"] <= max_price for item in data)


async def test_read_order_items_by_quantity(async_client: AsyncClient, create_order_item_fixture):
    quantity = 2
    response = await async_client.get(f"/order_items/quantity/{quantity}")
    assert response.status_code == 200

    data = response.json()
    assert any(item["quantity"] == quantity for item in data)


async def test_read_nonexistent_order_item(async_client: AsyncClient):
    response = await async_client.get("/order_items/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "OrderItem not found"