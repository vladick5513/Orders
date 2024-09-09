from api.order_items.schemas import OrderItemCreate, OrderItemUpdate
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import OrderItem


async def create_order_item(db: AsyncSession, order_item: OrderItemCreate):
    db_order_items = OrderItem(**order_item.model_dump())
    db.add(db_order_items)
    await db.commit()
    await db.refresh(db_order_items)
    return db_order_items

async def read_order_item(db: AsyncSession, order_item_id: int):
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if order_item is None:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    return order_item

async def update_order_item(db: AsyncSession, order_item_id: int, order_item: OrderItemUpdate):
    db_order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if db_order_item is None:
        raise HTTPException(status_code=404, detail="OrderItem")
    for key, value in order_item.model_dump(exclude_unset=True).items():
        setattr(db_order_items, key, value)
        await db.commit()
        await db.refresh(db_order_items)
        return db_order_item

async def delete_order_item(db: AsyncSession, order_item_id: int):
    db_order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if db_order_item is None:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    await db.delete(db_order_item)
    await db.commit()
    return db_order_item
