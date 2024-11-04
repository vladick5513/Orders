import pytest
from httpx import AsyncClient

async def test_create_customer(async_client: AsyncClient, customer_data_fixture):
    response = await async_client.post("/customers/", json=customer_data_fixture)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["name"] == customer_data_fixture["name"]
    assert data["email"] == customer_data_fixture["email"]
    assert "id" in data

    return data["id"]

async def test_get_customer_by_id(async_client: AsyncClient, customer_data_fixture):
    customer_id = await test_create_customer(async_client, customer_data_fixture)
    response = await async_client.get(f"/customers/{customer_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["id"] == customer_id
    assert data["name"] == customer_data_fixture["name"]

async def test_update_customer(async_client: AsyncClient, customer_data_fixture, updated_customer_data_fixture):
    customer_id = await test_create_customer(async_client, customer_data_fixture)
    response = await async_client.put(f"/customers/{customer_id}", json=updated_customer_data_fixture)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["name"] == updated_customer_data_fixture["name"]
    assert data["email"] == updated_customer_data_fixture["email"]

async def test_delete_customer(async_client: AsyncClient, customer_data_fixture):
    customer_id = await test_create_customer(async_client, customer_data_fixture)
    response = await async_client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    response = await async_client.get(f"/customers/{customer_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"

async def test_get_all_customers(async_client: AsyncClient, customer_data_fixture):
    await test_create_customer(async_client, customer_data_fixture)
    await test_create_customer(async_client, customer_data_fixture)
    response = await async_client.get("/customers/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Ожидаем хотя бы 2 клиента в базе данных

async def test_get_nonexistent_customer(async_client: AsyncClient):
    response = await async_client.get("/customers/999999")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"

async def test_create_customer_invalid_data(async_client: AsyncClient):
    invalid_data = {
        "name": "",
        "email": "invalid-email",
        "phone": 786,
        "address": "123 Main St"
    }
    response = await async_client.post("/customers/", json=invalid_data)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"