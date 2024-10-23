from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.shipping.crud import create_shipping, read_shipping, update_shipping, delete_shipping, read_all_shippings, read_shippings_by_status
from api.shipping.schemas import ShippingCreate, ShippingUpdate, ShippingResponse
from src.database import get_db

router = APIRouter(prefix="/shipping", tags=["Shipping"])

@router.post("/", response_model=ShippingResponse)
async def create_shipping_endpoint(shipping: ShippingCreate, db: AsyncSession = Depends(get_db)):
    return await create_shipping(db, shipping)

@router.get("/{shipping_id}", response_model=ShippingResponse)
async def read_shipping_endpoint(shipping_id: int, db: AsyncSession = Depends(get_db)):
    return await read_shipping(db, shipping_id)

@router.get("/", response_model=list[ShippingResponse])
async def read_all_shippings_endpoint(db: AsyncSession = Depends(get_db)):
    return await read_all_shippings(db)

@router.get("/status/", response_model=list[ShippingResponse])
async def read_shippings_by_status_endpoint(status: str, db: AsyncSession = Depends(get_db)):
    return await read_shippings_by_status(db, status)

@router.put("/{shipping_id}", response_model=ShippingResponse)
async def update_shipping_endpoint(shipping_id: int, shipping: ShippingUpdate, db: AsyncSession = Depends(get_db)):
    return await update_shipping(db, shipping_id, shipping)

@router.delete("/{shipping_id}", response_model=ShippingResponse)
async def delete_shipping_endpoint(shipping_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_shipping(db, shipping_id)