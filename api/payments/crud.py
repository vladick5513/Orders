from fastapi import HTTPException
from sqlalchemy.future import select

from sqlalchemy.ext.asyncio import AsyncSession
from api.payments.schemas import PaymentCreate, PaymentUpdate
from src.models import Payment

async def create_payment(db: AsyncSession, payment: PaymentCreate):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment

async def read_payment(db: AsyncSession, payment_id: int):
    result = await db.execute(select(Payment).filter(Payment.id==payment_id))
    payment = result.scalar_one_or_none()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

async def read_payments_by_order_id(db: AsyncSession, order_id: int):
    result = await db.execute(select(Payment).filter(Payment.order_id==order_id))
    payments = result.scalars().all()
    if not payments:
        raise HTTPException(status_code=404, detail=f"No payments found in the amount range {min_amount} - {max_amount}")
    return payments

async def read_payments_by_amount_range(db: AsyncSession, min_amount: float, max_amount: float):
    result = await db.execute(select(Payment).filter(Payment.amount.between(min_amount, max_amount)))
    payments = result.scalars().all()
    if not payments:
        raise HTTPException(status_code=404, detail=f"No payments found in the amount range {min_amount} - {max_amount}")
    return payments

async def update_payment(db: AsyncSession, payment_id: int, payment: PaymentUpdate):
    result = await db.execute(select(Payment).filter(Payment.id == payment_id))
    db_payment = result.scalar_one_or_none()
    if not db_payment:
        return None
    for key, value in payment.dict(exclude_unset=True).items():
        setattr(db_payment, key, value)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment

async def delete_payment(db: AsyncSession, payment_id: int):
    result = await db.execute(select(Payment).filter(Payment.id == payment_id))
    db_payment = result.scalar_one_or_none()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    await db.delete(db_payment)
    await db.commit()
    return db_payment