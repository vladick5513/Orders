from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.models import Customers
from api.customers.schemas import CustomerCreate, CustomerUpdate



async def create_customer(db: AsyncSession, customer: CustomerCreate):
    db_customer = Customers(**customer.model_dump())
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

async def read_customer(db: AsyncSession, customer_id:int):
    result = await db.execute(select(Customers).filter(Customers.id == customer_id))
    customer = result.scalar_one_or_none()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

async def update_customer(db: AsyncSession, customer_id:int, customer: CustomerUpdate):
    result = await db.execute(select(Customers).filter(Customers.id==customer_id))
    db_customer = result.scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

async def delete_customer(db: AsyncSession, customer_id: int):
    result = await db.execute(select(Customers).filter(Customers.id==customer_id))
    db_customer = result.scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    await db.delete(db_customer)
    await db.commit()
    return db_customer