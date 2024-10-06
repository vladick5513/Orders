import pytest
from api.payments.crud import read_payment, update_payment, delete_payment
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from api.payments.schemas import PaymentUpdate

async def test_create_payment(async_session: AsyncSession, setup_data_payment):
    payment = setup_data_payment["payment"]

    assert payment is not None
    assert payment.order_id == setup_data_payment["order"].id
    assert payment.amount == 200.50
    assert payment.payment_method == "Credit Card"



async def test_read_payment(async_session: AsyncSession, setup_data_payment):
    payment = setup_data_payment["payment"]

    read_payment_result = await read_payment(async_session, payment.id)

    assert read_payment_result is not None
    assert read_payment_result.id == payment.id
    assert read_payment_result.order_id == setup_data_payment["order"].id
    assert read_payment_result.amount == payment.amount
    assert read_payment_result.payment_method == payment.payment_method



async def test_update_payment(async_session: AsyncSession, setup_data_payment):
    payment = setup_data_payment["payment"]
    order = setup_data_payment["order"]

    update_data = PaymentUpdate(
        order_id=order.id,
        amount=250.75,
        payment_method="Debit Card"
    )

    updated_payment = await update_payment(async_session, payment.id, update_data)

    assert updated_payment is not None
    assert updated_payment.id == payment.id
    assert updated_payment.amount == update_data.amount
    assert updated_payment.payment_method == update_data.payment_method



async def test_delete_payment(async_session: AsyncSession, setup_data_payment):
    payment = setup_data_payment["payment"]

    deleted_payment = await delete_payment(async_session, payment.id)

    assert deleted_payment is not None
    assert deleted_payment.id == payment.id

    with pytest.raises(HTTPException):
        await read_payment(async_session, payment.id)