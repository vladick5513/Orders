from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.order_items.crud import create_order_item, read_order_item, update_order_item, delete_order_item,read_order_items_by_price_range, read_order_items_by_quantity
from api.order_items.schemas import OrderItemCreate, OrderItemUpdate, OrderItemResponse
from src.database import get_db

router = APIRouter(prefix="/order_items", tags=["Order Items"])

@router.post("/", response_model=OrderItemResponse)
async def create_order_item_endpoint(order_item: OrderItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_order_item(db, order_item)

@router.get("/price_range", response_model=list [OrderItemResponse])
async def read_order_items_by_price_range_endpoint(min_price: float, max_price: float, db: AsyncSession = Depends(get_db)):
    return await read_order_items_by_price_range(db, min_price, max_price)

@router.get("/quantity/{quantity}", response_model=list[OrderItemResponse])
async def read_order_items_by_quantity_endpoint(quantity: int, db: AsyncSession = Depends(get_db)):
    return await read_order_items_by_quantity(db, quantity)


@router.get("/{order_item_id}", response_model=OrderItemResponse)
async def read_order_item_endpoint(order_item_id: int, db: AsyncSession = Depends(get_db)):
    return await read_order_item(db, order_item_id)

@router.put("/{order_item_id}", response_model=OrderItemResponse)
async def update_order_item_endpoint(order_item_id: int, order_item: OrderItemUpdate, db: AsyncSession = Depends(get_db)):
    return await update_order_item(db, order_item_id, order_item)

@router.delete("/{order_item_id}", response_model=OrderItemResponse)
async def delete_order_item_endpoint(order_item_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_order_item(db, order_item_id)