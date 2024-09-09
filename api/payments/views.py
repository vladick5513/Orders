from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.payments.crud import create_payment, read_payment, update_payment, delete_payment
from api.payments.schemas import PaymentCreate, PaymentUpdate, PaymentResponse
from src.database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
async def create_payment_endpoint(payment: PaymentCreate, db: AsyncSession = Depends(get_db)):
    return await create_payment(db, payment)

@router.get("/{payment_id}", response_model=PaymentResponse)
async def read_payment_endpoint(payment_id: int, db: AsyncSession = Depends(get_db)):
    return await read_payment(db, payment_id)

@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment_endpoint(payment_id: int, payment: PaymentUpdate, db: AsyncSession = Depends(get_db)):
    return await update_payment(db, payment_id, payment)

@router.delete("/{payment_id}", response_model=PaymentResponse)
async def delete_payment_endpoint(payment_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_payment(db, payment_id)