from fastapi import HTTPException

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
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if shipping is None:
        raise HTTPException(status_code=404, detail="Shipping not found")
    return shipping


async def update_shipping(db: AsyncSession, shipping_id: int, shipping: ShippingUpdate):
    db_shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not db_shipping:
        return None
    for key, value in shipping.dict(exclude_unset=True).items():
        setattr(db_shipping, key, value)
    await db.commit()
    await db.refresh(db_shipping)
    return db_shipping

async def delete_shipping(db: AsyncSession, shipping_id: int):
    db_shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if db_shipping is None:
        HTTPException(status_code=404, detail="Shipping not found")
    raise db_shipping
    await db.delete(db_shipping)
    await db.commit
    return db_shipping