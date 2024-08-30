from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.customers.crud import create_customer, read_customer, update_customer, delete_customer
from src.database import get_db
from api.customers.schemas import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse)
def create_customer_endpoint(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)

# Чтение
@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer_endpoint(customer_id: int, db: Session = Depends(get_db)):
    return read_customer(db, customer_id)

# Обновление
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer_endpoint(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    return update_customer(db, customer_id, customer)

# Удаление
@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer_endpoint(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(db, customer_id)