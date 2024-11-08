import pytest
from httpx import AsyncClient



async def test_create_payment(async_client: AsyncClient, create_order_fixture):
    payment_data = {
        "order_id": create_order_fixture.id,
        "amount": 150.0,
        "payment_method": "paypal"
    }
    response = await async_client.post("/payments/", json=payment_data)
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == create_order_fixture.id
    assert data["amount"] == payment_data["amount"]
    assert data["payment_method"] == payment_data["payment_method"]


async def test_read_payment(async_client: AsyncClient, create_payment_fixture):
    response = await async_client.get(f"/payments/{create_payment_fixture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == create_payment_fixture.id
    assert data["order_id"] == create_payment_fixture.order_id
    assert data["amount"] == create_payment_fixture.amount
    assert data["payment_method"] == create_payment_fixture.payment_method


async def test_read_payments_by_order_id(async_client: AsyncClient, create_order_fixture, create_payment_fixture):
    response = await async_client.get(f"/payments/order/{create_order_fixture.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for payment in data:
        assert payment["order_id"] == create_order_fixture.id


async def test_read_payments_by_amount_range(async_client: AsyncClient, create_payment_fixture):
    min_amount = 50.0
    max_amount = 200.0
    response = await async_client.get(f"/payments/amount_range/?min_amount={min_amount}&max_amount={max_amount}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for payment in data:
        assert min_amount <= payment["amount"] <= max_amount


async def test_update_payment(async_client: AsyncClient, create_payment_fixture):
    updated_data = {
        "order_id": create_payment_fixture.order_id,
        "amount": 200.0,
        "payment_method": "bank_transfer"
    }
    response = await async_client.put(f"/payments/{create_payment_fixture.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == create_payment_fixture.id
    assert data["amount"] == updated_data["amount"]
    assert data["payment_method"] == updated_data["payment_method"]


async def test_delete_payment(async_client: AsyncClient, create_payment_fixture):
    response = await async_client.delete(f"/payments/{create_payment_fixture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == create_payment_fixture.id

    response = await async_client.get(f"/payments/{create_payment_fixture.id}")
    assert response.status_code == 404