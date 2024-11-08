import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

async def test_create_shipping(async_client: AsyncClient, create_order_fixture):
    shipping_data = {
        "order_id": create_order_fixture.id,
        "shipping_address": "456 Example Ave.",
        "shipping_date": datetime.utcnow().isoformat(),
        "delivery_date": (datetime.utcnow() + timedelta(days=3)).isoformat(),
        "status": "in_transit"
    }
    response = await async_client.post("/shipping/", json=shipping_data)
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == create_order_fixture.id
    assert data["shipping_address"] == shipping_data["shipping_address"]
    assert data["status"] == shipping_data["status"]


async def test_read_shipping(async_client: AsyncClient, create_shipping_fixture):
    response = await async_client.get(f"/shipping/{create_shipping_fixture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == create_shipping_fixture.id
    assert data["order_id"] == create_shipping_fixture.order_id
    assert data["status"] == create_shipping_fixture.status


async def test_read_all_shippings(async_client: AsyncClient, create_shipping_fixture):
    response = await async_client.get("/shipping/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(shipping["id"] == create_shipping_fixture.id for shipping in data)


async def test_read_shippings_by_status(async_client: AsyncClient, create_shipping_fixture):
    status = create_shipping_fixture.status
    response = await async_client.get(f"/shipping/status/?status={status}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for shipping in data:
        assert shipping["status"] == status


async def test_update_shipping(async_client: AsyncClient, create_shipping_fixture):
    updated_data = {
        "order_id": create_shipping_fixture.order_id,
        "shipping_address": "789 Updated Rd.",
        "status": "delivered",
        "shipping_date": create_shipping_fixture.shipping_date.isoformat(),
        "delivery_date": create_shipping_fixture.delivery_date.isoformat()
    }
    response = await async_client.put(f"/shipping/{create_shipping_fixture.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == create_shipping_fixture.id
    assert data["shipping_address"] == updated_data["shipping_address"]
    assert data["status"] == updated_data["status"]


async def test_delete_shipping(async_client: AsyncClient, create_shipping_fixture):
    response = await async_client.delete(f"/shipping/{create_shipping_fixture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == create_shipping_fixture.id

    # Verify that the shipping record has been deleted
    response = await async_client.get(f"/shipping/{create_shipping_fixture.id}")
    assert response.status_code == 404