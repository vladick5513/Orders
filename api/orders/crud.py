from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.models import Order
from api.orders.schemas import OrderCreate, OrderUpdate

async def create_order(db: AsyncSession, order: OrderCreate):
    db_order = Order(**order.model_dump())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

async def read_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).filter(Order.id==order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

async def update_order(db: AsyncSession, order_id: int, order: OrderUpdate):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    db_order = result.scalar_one_or_none()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    await db.commit()
    await db.refresh(db_order)
    return db_order

async def delete_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    db_order = result.scalar_one_or_none()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    await db.delete(db_order)
    await db.commit()
    return db_order