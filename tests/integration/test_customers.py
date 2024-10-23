import pytest
from httpx import AsyncClient
from api.customers.schemas import CustomerCreate, CustomerUpdate

async def test_create_customer(async_client: AsyncClient):
    customer_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+123456789",
        "address": "123 Main St"
    }

    response = await async_client.post("/customers/", json=customer_data)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["email"] == customer_data["email"]
    assert "id" in data

    customer_id = data["id"]
    return customer_id