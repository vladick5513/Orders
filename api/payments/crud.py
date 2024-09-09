from fastapi import HTTPException

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
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

async def update_payment(db: AsyncSession, payment_id: int, payment: PaymentUpdate):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        return None
    for key, value in payment.dict(exclude_unset=True).items():
        setattr(db_payment, key, value)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment

async def delete_payment(db: AsyncSession, payment_id: int):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    await db.delete(db_payment)
    await db.commit()
    return db_payment