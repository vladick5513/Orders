from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.customers.crud import create_customer, read_customer, update_customer, delete_customer
from src.database import get_db
from api.customers.schemas import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse)
async def create_customer_endpoint(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    return await create_customer(db, customer)

# Чтение
@router.get("/{customer_id}", response_model=CustomerResponse)
async def read_customer_endpoint(customer_id: int, db: AsyncSession = Depends(get_db)):
   return await read_customer(db, customer_id)

# Обновление
@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer_endpoint(customer_id: int, customer: CustomerUpdate, db: AsyncSession = Depends(get_db)):
    return await update_customer(db, customer_id, customer)

# Удаление
@router.delete("/{customer_id}", response_model=CustomerResponse)
async def delete_customer_endpoint(customer_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_customer(db, customer_id)