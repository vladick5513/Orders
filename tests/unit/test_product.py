import pytest
from api.products.crud import create_product, read_product, update_product, delete_product
from api.products.schemas import ProductCreate, ProductUpdate
from src.config import settings
from fastapi import HTTPException


@pytest.mark.asycio
async def test_create_product(async_session, setup_db):
    product_data = ProductCreate(
        name="Test Product",
        description="This is a test product",
        price=1000,
        stock_quantity=10
    )
    product = await create_product(async_session, product_data)
    assert product is not None
    assert product.name == "Test Product"
    assert product.price == 1000
    assert product.stock_quantity == 10

@pytest.mark.asycio
async def test_read_product(async_session):
    product_data = ProductCreate(
        name="Test Product",
        description="This is a test product",
        price=1000,
        stock_quantity=10
    )
    product = await create_product(async_session, product_data)
    fetched_product = await read_product(async_session, product.id)
    assert fetched_product is not None
    assert fetched_product.id == product.id
    assert fetched_product.name == "Test Product"

@pytest.mark.asycio
async def test_update_product(async_session):
    product_data = ProductCreate(
        name="Old Product",
        description="This is an old product",
        price=500,
        stock_quantity=5
    )
    product = await create_product(async_session, product_data)
    updated_data = ProductUpdate(
        name="Updated Product",
        description="This is an new product",
        price=1500,
        stock_quantity=20
    )
    updated_product = await update_product(async_session, product.id, updated_data)
    assert updated_product is not None
    assert updated_product.name == "Updated Product"
    assert updated_product.price == 1500
    assert updated_product.stock_quantity == 20


@pytest.mark.asyncio
async def test_delete_product(async_session):
    product_data = ProductCreate(
        name="Test Product",
        description="This is a test product",
        price=1000,
        stock_quantity=10
    )
    product = await create_product(async_session, product_data)
    await delete_product(async_session, product.id)

    with pytest.raises(HTTPException) as exc_info:
        await read_product(async_session, product.id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Product not found"


