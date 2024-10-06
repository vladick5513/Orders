import pytest
from api.products.crud import create_product, read_product, update_product, delete_product
from api.products.schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException




async def test_create_product(async_session, setup_product):
    product = setup_product
    assert product is not None
    assert product.name == "Test Product"
    assert product.price == 1000
    assert product.stock_quantity == 10


async def test_read_product(async_session, setup_product):
    product = setup_product
    fetched_product = await read_product(async_session, product.id)
    assert fetched_product is not None
    assert fetched_product.id == product.id
    assert fetched_product.name == "Test Product"


async def test_update_product(async_session, setup_product):
    product = setup_product
    updated_data = ProductUpdate(
        name="Updated Product",
        description="This is a new product",
        price=1500,
        stock_quantity=20
    )
    updated_product = await update_product(async_session, product.id, updated_data)
    assert updated_product is not None
    assert updated_product.name == "Updated Product"
    assert updated_product.price == 1500
    assert updated_product.stock_quantity == 20


async def test_delete_product(async_session, setup_product):
    product = setup_product
    await delete_product(async_session, product.id)

    with pytest.raises(HTTPException) as exc_info:
        await read_product(async_session, product.id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Product not found"


