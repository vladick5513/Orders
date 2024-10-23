from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.payments.crud import create_payment, read_payment, update_payment, delete_payment, read_payments_by_order_id, read_payments_by_amount_range
from api.payments.schemas import PaymentCreate, PaymentUpdate, PaymentResponse
from src.database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
async def create_payment_endpoint(payment: PaymentCreate, db: AsyncSession = Depends(get_db)):
    return await create_payment(db, payment)

@router.get("/{payment_id}", response_model=PaymentResponse)
async def read_payment_endpoint(payment_id: int, db: AsyncSession = Depends(get_db)):
    return await read_payment(db, payment_id)

@router.get("/order/{order_id}", response_model=list[PaymentResponse])
async def read_payments_by_order_id_endpoint(order_id: int, db: AsyncSession = Depends(get_db)):
    return await read_payments_by_order_id(db, order_id)

@router.get("/amount_range/", response_model=list[PaymentResponse])
async def read_payments_by_amount_range_endpoint(min_amount: float, max_amount: float, db: AsyncSession = Depends(get_db)):
    return await read_payments_by_amount_range(db, min_amount, max_amount)

@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment_endpoint(payment_id: int, payment: PaymentUpdate, db: AsyncSession = Depends(get_db)):
    return await update_payment(db, payment_id, payment)

@router.delete("/{payment_id}", response_model=PaymentResponse)
async def delete_payment_endpoint(payment_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_payment(db, payment_id)