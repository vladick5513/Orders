from api.order_items.schemas import OrderItemCreate, OrderItemUpdate
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import OrderItem


async def create_order_item(db: AsyncSession, order_item: OrderItemCreate):
    db_order_items = OrderItem(**order_item.model_dump())
    db.add(db_order_items)
    await db.commit()
    await db.refresh(db_order_items)
    return db_order_items

async def read_order_items_by_price_range(db: AsyncSession, min_price: float, max_price: float):
    result = await db.execute(select(OrderItem).filter(OrderItem.price >= min_price, OrderItem.price <= max_price))
    order_items = result.scalars().all()
    return order_items

async def read_order_items_by_quantity(db: AsyncSession, quantity: int):
    result = await db.execute(select(OrderItem).filter(OrderItem.quantity == quantity))
    order_items = result.scalars().all()
    if not order_items:
        raise HTTPException(status_code=404, detail=f"No OrderItems found with quantity {quantity}")
    return order_items


async def read_order_item(db: AsyncSession, order_item_id: int):
    result = await db.execute(select(OrderItem).filter(OrderItem.id == order_item_id))
    order_item = result.scalar_one_or_none()
    if order_item is None:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    return order_item

async def update_order_item(db: AsyncSession, order_item_id: int, order_item: OrderItemUpdate):
    result = await db.execute(select(OrderItem).filter(OrderItem.id == order_item_id))
    db_order_item = result.scalar_one_or_none()
    if db_order_item is None:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    for key, value in order_item.model_dump(exclude_unset=True).items():
        setattr(db_order_item, key, value)
    await db.commit()
    await db.refresh(db_order_item)
    return db_order_item

async def delete_order_item(db: AsyncSession, order_item_id: int):
    result = await db.execute(select(OrderItem).filter(OrderItem.id == order_item_id))
    db_order_item = result.scalar_one_or_none()
    if db_order_item is None:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    await db.delete(db_order_item)
    await db.commit()
    return db_order_item
