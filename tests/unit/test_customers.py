import pytest
from api.customers.crud import create_customer, read_customer, update_customer, delete_customer
from api.customers.schemas import CustomerCreate, CustomerUpdate
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_create_customer(async_session, setup_db):
    # Данные для создания нового клиента
    customer_data = CustomerCreate(
        name="Alice Smith",
        email="alice@example.com",
        phone="987654321",
        address="456 Elm Street"
    )

    # Создание клиента
    customer = await create_customer(async_session, customer_data)

    # Проверяем, что клиент был успешно создан
    assert customer is not None
    assert customer.name == customer_data.name
    assert customer.email == customer_data.email
    assert customer.phone == customer_data.phone
    assert customer.address == customer_data.address


@pytest.mark.asyncio
async def test_get_customer(async_session):
    # Предполагаем, что в базе данных уже существует клиент
    customer_data = CustomerCreate(
        name="John Doe",
        email="john@example.com",
        phone="123456789",
        address="123 Main Street"
    )

    # Сначала создаем клиента
    customer = await create_customer(async_session, customer_data)

    # Теперь пытаемся получить клиента по его ID
    fetched_customer = await read_customer(async_session, customer.id)

    # Проверяем, что клиент успешно найден
    assert fetched_customer is not None
    assert fetched_customer.id == customer.id
    assert fetched_customer.name == customer.name


@pytest.mark.asyncio
async def test_update_customer(async_session):
    # Данные для нового клиента
    customer_data = CustomerCreate(
        name="Alice Johnson",
        email="alice.johnson@example.com",
        phone="987654321",
        address="789 Oak Street"
    )

    # Создаем клиента
    customer = await create_customer(async_session, customer_data)

    # Обновляем информацию о клиенте
    update_data = CustomerUpdate(
        name="Alice Updated",
        email="alice.updated@example.com",
        phone="123123123",
        address="Updated Street"
    )

    updated_customer = await update_customer(async_session, customer.id, update_data)

    # Проверяем, что информация о клиенте обновилась
    assert updated_customer is not None
    assert updated_customer.name == update_data.name
    assert updated_customer.email == update_data.email
    assert updated_customer.phone == update_data.phone
    assert updated_customer.address == update_data.address

@pytest.mark.asyncio
async def test_delete_customer(async_session):
    customer_data = CustomerCreate(
        name="Alice Promo",
        email="alice.promo@example.com",
        phone="123123123",
        address="Updated Street"
    )
    customer = await create_customer(async_session, customer_data)

    await delete_customer(async_session, customer.id)
    with pytest.raises(HTTPException) as exc_info:
        await read_customer(async_session, customer.id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Customer not found"


