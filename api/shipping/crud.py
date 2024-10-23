from fastapi import HTTPException
from sqlalchemy.future import select

from sqlalchemy.ext.asyncio import AsyncSession
from api.shipping.schemas  import ShippingCreate, ShippingUpdate
from src.models import Shipping

async def create_shipping(db: AsyncSession, shipping: ShippingCreate):
    db_shipping = Shipping(**shipping.dict())
    db.add(db_shipping)
    await db.commit()
    await db.refresh(db_shipping)
    return db_shipping

async def read_shipping(db: AsyncSession, shipping_id: int):
    result = await db.execute(select(Shipping).filter(Shipping.id==shipping_id))
    shipping = result.scalar_one_or_none()
    if shipping is None:
        raise HTTPException(status_code=404, detail="Shipping not found")
    return shipping

async def read_all_shippings(db: AsyncSession):
    result = await db.execute(select(Shipping))
    shippings = result.scalars().all()
    if not shippings:
        raise HTTPException(status_code=404, detail="No shipping records found")
    return shippings


async def read_shippings_by_status(db: AsyncSession, status: str):
    result = await db.execute(select(Shipping).filter(Shipping.status == status))
    shippings = result.scalars().all()
    if not shippings:
        raise HTTPException(status_code=404, detail=f"No shipping records with status '{status}' found")
    return shippings


async def update_shipping(db: AsyncSession, shipping_id: int, shipping: ShippingUpdate):
    result = await db.execute(select(Shipping).filter(Shipping.id == shipping_id))
    db_shipping = result.scalar_one_or_none()
    if not db_shipping:
        return None
    for key, value in shipping.dict(exclude_unset=True).items():
        setattr(db_shipping, key, value)
    await db.commit()
    await db.refresh(db_shipping)
    return db_shipping

async def delete_shipping(db: AsyncSession, shipping_id: int):
    result = await db.execute(select(Shipping).filter(Shipping.id == shipping_id))
    db_shipping = result.scalar_one_or_none()
    if db_shipping is None:
        raise HTTPException(status_code=404, detail="Shipping not found")
    await db.delete(db_shipping)
    await db.commit()
    return db_shipping