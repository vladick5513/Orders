import pytest
from api.products.schemas import ProductResponse
from httpx import AsyncClient
from api.customers.schemas import CustomerCreate
from api.customers.schemas import CustomerResponse
from api.orders.schemas import OrderResponse
from api.payments.schemas import PaymentResponse
from api.shipping.schemas import ShippingResponse
from datetime import datetime, timedelta

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

@pytest.fixture
async def create_product_fixture(async_client: AsyncClient):
    product_data = {
        "name": "Sample Product",
        "description": "A sample product for testing",
        "price": 100,
        "stock_quantity": 50
    }
    response = await async_client.post("/products/", json=product_data)
    assert response.status_code == 200
    return ProductResponse(**response.json())

@pytest.fixture
async def create_order_item_fixture(async_client: AsyncClient, create_order_fixture, create_product_fixture):
    order_item_data = {
        "order_id": create_order_fixture.id,
        "product_id": create_product_fixture.id,
        "quantity": 2,
        "price": 100.0,
        "total_price": 200.0
    }
    response = await async_client.post("/order_items/", json=order_item_data)
    return response.json()

@pytest.fixture
async def create_payment_fixture(async_client: AsyncClient, create_order_fixture):
    payment_data = {
        "order_id": create_order_fixture.id,
        "amount": 100.0,
        "payment_method": "credit_card"
    }
    response = await async_client.post("/payments/", json=payment_data)
    assert response.status_code == 200
    return PaymentResponse(**response.json())

@pytest.fixture
async def create_shipping_fixture(async_client: AsyncClient, create_order_fixture):
    shipping_data = {
        "order_id": create_order_fixture.id,
        "shipping_address": "123 Test St.",
        "shipping_date": datetime.utcnow().isoformat(),
        "delivery_date": (datetime.utcnow() + timedelta(days=2)).isoformat(),
        "status": "pending"
    }
    response = await async_client.post("/shipping/", json=shipping_data)
    assert response.status_code == 200
    return ShippingResponse(**response.json())


