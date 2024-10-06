import pytest
from api.customers.schemas import CustomerCreate
from api.orders.schemas import OrderCreate
from api.payments.crud import create_payment
from api.orders.crud import create_order
from api.customers.crud import create_customer
from api.payments.schemas import PaymentCreate
from api.products.schemas import ProductCreate
from api.products.crud import create_product
from api.shipping.schemas import ShippingCreate
from api.shipping.crud import create_shipping

@pytest.fixture
async def setup_customer_order_shipping(async_session):
    # Создаем клиента
    customer_data = CustomerCreate(
        name="John Doe",
        email="john@example.com",
        phone="123456789",
        address="123 Main Street"
    )
    customer = await create_customer(async_session, customer_data)

    # Создаем заказ
    order_data = OrderCreate(
        customer_id=customer.id,
        status="Processing",
        total_amount=1500
    )
    order = await create_order(async_session, order_data)

    # Создаем доставку
    shipping_data = ShippingCreate(
        order_id=order.id,
        shipping_address="Test Address",
        shipping_date="2024-09-30T00:00:00",
        delivery_date="2024-10-01T00:00:00",
        status="Pending"
    )
    shipping = await create_shipping(async_session, shipping_data)

    return customer, order, shipping


# Фикстура для создания продукта, клиента и заказа
@pytest.fixture
async def setup_product_customer_order(async_session):
    # Создание клиента
    customer_data = CustomerCreate(
        name="John Doe",
        email="john.doe@example.com",
        phone="1234567890",
        address="123 Main St"
    )
    customer = await create_customer(async_session, customer_data)

    # Создание продукта
    product_data = ProductCreate(
        name="Test Product",
        description="This is a test product",
        price=500,
        stock_quantity=10
    )
    product = await create_product(async_session, product_data)

    # Создание заказа с валидным customer_id
    order_data = OrderCreate(
        customer_id=customer.id,
        status="Pending",
        total_amount=1000
    )
    order = await create_order(async_session, order_data)

    # Возвращаем продукт, клиента и заказ
    return product, customer, order


@pytest.fixture
async def setup_product(async_session):
    product_data = ProductCreate(
        name="Test Product",
        description="This is a test product",
        price=1000,
        stock_quantity=10
    )
    product = await create_product(async_session, product_data)
    return product

@pytest.fixture
async def setup_customer_and_order(async_session):
    customer_data = CustomerCreate(
        name="John Doe",
        email="john@example.com",
        phone="123456789",
        address="123 Main Street"
    )
    customer = await create_customer(async_session, customer_data)

    order_data = OrderCreate(
        customer_id=customer.id,
        status="Processing",
        total_amount=1500
    )
    order = await create_order(async_session, order_data)

    return customer, order



@pytest.fixture
def setup_customer_data():
    return CustomerCreate(
        name="Alice Smith",
        email="alice@example.com",
        phone="987654321",
        address="456 Elm Street"
    )


@pytest.fixture(scope="function")
async def setup_data_payment(async_session):
    # Создание клиента
    customer_data = CustomerCreate(
        name="John Doe",
        email="john@example.com",
        phone="123456789",
        address="123 Main Street"
    )
    customer = await create_customer(async_session, customer_data)

    # Создание заказа
    order_data = OrderCreate(
        customer_id=customer.id,
        status="Processing",
        total_amount=1500
    )
    order = await create_order(async_session, order_data)

    # Создание платежа
    payment_data = PaymentCreate(
        order_id=order.id,
        amount=200.50,
        payment_method="Credit Card"
    )
    payment = await create_payment(async_session, payment_data)

    return {
        "customer": customer,
        "order": order,
        "payment": payment
    }