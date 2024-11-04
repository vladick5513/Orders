import pytest
from httpx import AsyncClient

async def test_create_order(async_client: AsyncClient, create_customer_fixture):
    order_data = {
        "customer_id": create_customer_fixture.id,
        "status": "pending",
        "total_amount": 100.0
    }

    response = await async_client.post("/orders/", json=order_data)
    assert response.status_code == 200

    data = response.json()
    assert data["customer_id"] == create_customer_fixture.id
    assert data["status"] == order_data["status"]
    assert data["total_amount"] == order_data["total_amount"]

async def test_read_order(async_client: AsyncClient, create_order_fixture, create_customer_fixture):
    response = await async_client.get(f"/orders/{create_order_fixture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == create_order_fixture.id
    assert data["customer_id"] == create_customer_fixture.id
    assert data["status"] == create_order_fixture.status

async def test_update_order(async_client: AsyncClient, create_order_fixture, create_customer_fixture):
    updated_order_data = {
        "customer_id": create_customer_fixture.id,
        "status": "shipped",
        "total_amount": 150.0
    }
    response = await async_client.put(f"/orders/{create_order_fixture.id}", json=updated_order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == updated_order_data["customer_id"]
    assert data["status"] == updated_order_data["status"]
    assert data["total_amount"] == updated_order_data["total_amount"]



async def test_delete_order(async_client: AsyncClient, create_order_fixture):
    response = await async_client.delete(f"/orders/{create_order_fixture.id}")
    assert response.status_code == 200
    response = await async_client.get(f"/orders/{create_order_fixture.id}")
    assert response.status_code == 404

async def test_read_orders_by_status(async_client: AsyncClient, create_order_fixture):
    response = await async_client.get(f"/orders/status/{create_order_fixture.status}")
    assert response.status_code == 200
    data = response.json()
    assert any(order["status"] == create_order_fixture.status for order in data)

async def test_read_orders_by_total_amount_range(async_client: AsyncClient, create_order_fixture):
    min_amount = 50.0
    max_amount = 150.0
    response = await async_client.get(f"/orders/total_amount/?min_amount={min_amount}&max_amount={max_amount}")
    assert response.status_code == 200
    data = response.json()
    assert any(min_amount <= order["total_amount"] <= max_amount for order in data)

async def test_read_nonexistent_order(async_client: AsyncClient):
    response = await async_client.get("/orders/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"