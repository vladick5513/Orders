from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.payments.crud import create_payment, read_payment, update_payment, delete_payment
from api.payments.schemas import PaymentCreate, PaymentUpdate, PaymentResponse
from src.database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=int)
def create_payment_endpoint(payment: PaymentCreate, db: Session = Depends(get_db)):
    return create_payment(db, payment)

@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment_endpoint(payment_id: int, db: Session = Depends(get_db)):
    return read_payment(db, payment_id)

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment_endpoint(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    return update_payment(db, payment_id, payment)

@router.delete("/{payment_id}")
def delete_payment_endpoint(payment_id: int, db: Session = Depends(get_db)):
    return delete_payment(db, payment_id)