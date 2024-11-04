import pytest
from httpx import AsyncClient
from api.customers.schemas import CustomerCreate
from api.customers.schemas import CustomerResponse
from api.orders.schemas import OrderResponse

@pytest.fixture
def customer_data_fixture():
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+123456789",
        "address": "123 Main St"
    }

@pytest.fixture
def updated_customer_data_fixture():
    return {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": "+987654321",
        "address": "456 Elm St"
    }

@pytest.fixture
async def create_customer_fixture(async_client: AsyncClient):
    customer_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "address": "123 Main St"
    }
    response = await async_client.post("/customers/", json=customer_data)
    assert response.status_code == 200
    return CustomerResponse(**response.json())


@pytest.fixture
async def create_order_fixture(async_client: AsyncClient, create_customer_fixture):
    order_data = {
        "customer_id": create_customer_fixture.id,
        "status": "pending",
        "total_amount": 100.0
    }
    response = await async_client.post("/orders/", json=order_data)
    assert response.status_code == 200
    return OrderResponse(**response.json())



