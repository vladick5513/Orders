from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.orders.crud import create_order, read_order, update_order, delete_order
from src.database import get_db
from api.orders.schemas import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
async def create_order_endpoint(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await create_order(db, order)

@router.get("/{order_id}", response_model=OrderResponse)
async def read_order_endpoint(order_id: int, db: AsyncSession = Depends(get_db)):
    return await read_order(db, order_id)

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order_endpoint(order_id: int, order: OrderUpdate, db: AsyncSession = Depends(get_db)):
    return await update_order(db, order_id, order)

@router.delete("/{order_id}", response_model=OrderResponse)
async def delete_order_endpoint(order_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_order(db, order_id)