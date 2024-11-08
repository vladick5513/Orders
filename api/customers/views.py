from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.customers.crud import create_customer, read_customer, update_customer, delete_customer, read_customers_registered_recently, list_customers
from src.database import get_db
from api.customers.schemas import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse)
async def create_customer_endpoint(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    return await create_customer(db, customer)

@router.get("/recent", response_model=list [CustomerResponse])
async def read_customers_registered_recently_endpoint(days: int = 30, db: AsyncSession = Depends(get_db)):
    return await read_customers_registered_recently(db, days)

@router.get("/all", response_model=list[CustomerResponse])
async def list_customers_endpoint(db: AsyncSession = Depends(get_db)):
    return await list_customers(db)

@router.get("/{customer_id}", response_model=CustomerResponse)
async def read_customer_endpoint(customer_id: int, db: AsyncSession = Depends(get_db)):
   return await read_customer(db, customer_id)

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer_endpoint(customer_id: int, customer: CustomerUpdate, db: AsyncSession = Depends(get_db)):
    return await update_customer(db, customer_id, customer)

@router.delete("/{customer_id}", response_model=CustomerResponse)
async def delete_customer_endpoint(customer_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_customer(db, customer_id)