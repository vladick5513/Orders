import pytest
from api.products.crud import create_product
from api.orders.crud import create_order
from api.products.schemas import ProductCreate
from api.orders.schemas import OrderCreate
from api.order_items.crud import create_order_item, read_order_item, update_order_item, delete_order_item
from api.order_items.schemas import OrderItemCreate, OrderItemUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException




async def test_create_order_item(async_session: AsyncSession, setup_product_customer_order):
    product, customer, order = setup_product_customer_order  # Распаковываем продукт, клиента и заказ из фикстуры

    order_item_data = OrderItemCreate(
        order_id=order.id,
        product_id=product.id,
        quantity=2,
        price=product.price,
        total_price=product.price * 2
    )
    order_item = await create_order_item(async_session, order_item_data)

    assert order_item is not None
    assert order_item.order_id == order.id
    assert order_item.product_id == product.id
    assert order_item.quantity == 2
    assert order_item.total_price == product.price * 2


async def test_read_order_item(async_session: AsyncSession, setup_product_customer_order):
    product, customer, order = setup_product_customer_order  # Распаковываем продукт, клиента и заказ из фикстуры

    # Создаём OrderItem
    order_item_data = OrderItemCreate(
        order_id=order.id,
        product_id=product.id,
        quantity=2,
        price=product.price,
        total_price=product.price * 2
    )
    order_item = await create_order_item(async_session, order_item_data)

    # Читаем OrderItem
    fetched_order_item = await read_order_item(async_session, order_item.id)

    assert fetched_order_item is not None
    assert fetched_order_item.id == order_item.id
    assert fetched_order_item.order_id == order.id
    assert fetched_order_item.product_id == product.id
    assert fetched_order_item.quantity == 2
    assert fetched_order_item.total_price == product.price * 2


# Тест обновления OrderItem
async def test_update_order_item(async_session: AsyncSession, setup_product_customer_order):
    product, customer, order = setup_product_customer_order  # Распаковываем продукт, клиента и заказ из фикстуры

    # Создаём OrderItem
    order_item_data = OrderItemCreate(
        order_id=order.id,
        product_id=product.id,
        quantity=2,
        price=product.price,
        total_price=product.price * 2
    )
    order_item = await create_order_item(async_session, order_item_data)

    # Данные для обновления
    update_data = OrderItemUpdate(
        order_id=order.id,
        product_id=product.id,
        quantity=3,  # Обновляем количество
        price=product.price,
        total_price=product.price * 3
    )
    updated_order_item = await update_order_item(async_session, order_item.id, update_data)

    # Проверяем обновление
    assert updated_order_item is not None
    assert updated_order_item.id == order_item.id
    assert updated_order_item.quantity == 3  # Количество должно быть обновлено на 3
    assert updated_order_item.total_price == product.price * 3  # Итоговая цена также должна быть обновлена

async def test_delete_order_item(async_session: AsyncSession, setup_product_customer_order):
    product, customer, order = setup_product_customer_order  # Распаковываем продукт, клиента и заказ из фикстуры

    # Создаём OrderItem
    order_item_data = OrderItemCreate(
        order_id=order.id,
        product_id=product.id,
        quantity=2,
        price=product.price,
        total_price=product.price * 2
    )
    order_item = await create_order_item(async_session, order_item_data)

    # Удаляем OrderItem
    await delete_order_item(async_session, order_item.id)

    # Пытаемся прочитать удалённый OrderItem, ожидаем ошибку
    with pytest.raises(HTTPException) as exc_info:
        await read_order_item(async_session, order_item.id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "OrderItem not found"