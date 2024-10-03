import pytest
from api.customers.crud import create_customer
from api.customers.schemas import CustomerCreate
from api.orders.crud import create_order, read_order, delete_order, update_order
from api.orders.schemas import OrderCreate, OrderUpdate
from fastapi import HTTPException



async def test_create_order(async_session):
    customer_data = CustomerCreate(
        name="John Doe",
        email="john@example.com",
        phone="123456789",
        address="123 Main Street"
    )
    customer = await create_customer(async_session, customer_data)
    order_data = OrderCreate(
        customer_id = customer.id,
        status= "Processing",
        total_amount=1500
    )
    order = await create_order(async_session, order_data)
    assert order is not None
    assert order.customer_id == customer.id
    assert order.status == "Processing"
    assert order.total_amount == 1500


async def test_reade_order(async_session):
    customer_data = CustomerCreate(
        name="John Doe",
        email="doe@example.com",
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
    fetched_order = await read_order(async_session, order.id)

    assert fetched_order is not None
    assert fetched_order.id == order.id
    assert fetched_order.customer_id == customer.id
    assert fetched_order.status == "Processing"


async def test_update_order(async_session):
    customer_data = CustomerCreate(
        name="John Doe",
        email="john32@example.com",
        phone="123456789",
        address="123 Main Street"
    )
    customer = await create_customer(async_session, customer_data)


    order_data = OrderCreate(
        customer_id=customer.id,
        status="Processing",
        total_amount=1500.00
    )
    order = await create_order(async_session, order_data)

    update_data = OrderUpdate(
        status="Completed",
        total_amount=2000.00
    )
    updated_order = await update_order(async_session, order.id, update_data)

    # Проверяем обновление заказа
    assert updated_order is not None
    assert updated_order.status == "Completed"
    assert updated_order.total_amount == 2000.00


async def test_delete_order(async_session):
    customer_data = CustomerCreate(
        name="John Doe",
        email="doe99@example.com",
        phone="123456789",
        address="123 Main Street"
    )
    customer = await create_customer(async_session, customer_data)

    order_data = OrderCreate(
        customer_id=customer.id,
        status="Processing",
        total_amount=1500.00
    )
    order = await create_order(async_session, order_data)

    await delete_order(async_session, order.id)

    with pytest.raises(HTTPException) as exc_info:
        await read_order(async_session, order.id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Order not found"







