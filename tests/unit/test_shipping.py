import pytest
from api.orders.crud import create_order
from api.orders.schemas import OrderCreate
from api.shipping.crud import create_shipping
from api.shipping.schemas import ShippingCreate
from api.customers.schemas import CustomerCreate
from api.customers.crud import create_customer
from api.shipping.crud import read_shipping
from api.shipping.crud import delete_shipping
from api.shipping.crud import update_shipping
from api.shipping.schemas import ShippingUpdate
from fastapi import HTTPException




async def test_create_shipping(async_session, setup_customer_order_shipping):
    customer, order, shipping = setup_customer_order_shipping

    assert shipping is not None
    assert shipping.order_id == order.id

async def test_read_shipping(async_session, setup_customer_order_shipping):
    customer, order, shipping = setup_customer_order_shipping

    fetched_shipping = await read_shipping(async_session, shipping.id)

    assert fetched_shipping is not None
    assert fetched_shipping.id == shipping.id
    assert fetched_shipping.shipping_address == "Test Address"



async def test_update_shipping(async_session, setup_customer_order_shipping):
    customer, order, shipping = setup_customer_order_shipping

    update_data = ShippingUpdate(
        order_id=order.id,
        shipping_address="Updated Address",
        shipping_date="2024-09-30T12:00:00",
        delivery_date="2024-10-02T12:00:00",
        status="Shipped"
    )
    updated_shipping = await update_shipping(async_session, shipping.id, update_data)

    assert updated_shipping is not None
    assert updated_shipping.shipping_address == "Updated Address"
    assert updated_shipping.status == "Shipped"



async def test_delete_shipping(async_session, setup_customer_order_shipping):
    customer, order, shipping = setup_customer_order_shipping  # Используем фикстуру для создания заказов и доставки

    # Удаляем Shipping
    await delete_shipping(async_session, shipping.id)

    # Пытаемся прочитать удалённую запись Shipping, ожидаем ошибку
    with pytest.raises(HTTPException) as exc_info:
        await read_shipping(async_session, shipping.id)

    # Проверяем, что исключение 404 и сообщение верны
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Shipping not found"