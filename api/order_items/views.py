from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.order_items.crud import create_order_item, read_order_item, update_order_item, delete_order_item
from api.order_items.schemas import OrderItemCreate, OrderItemUpdate, OrderItemResponse
from src.database import get_db

router = APIRouter(prefix="/order_items", tags=["Order Items"])

@router.post("/", response_model=OrderItemResponse)
def create_order_item_endpoint(order_item: OrderItemCreate, db: Session = Depends(get_db)):
    return create_order_item(db, order_item)

@router.get("/{order_item_id}", response_model=OrderItemResponse)
def read_order_item_endpoint(order_item_id: int, db: Session = Depends(get_db)):
    return read_order_item(db, order_item_id)

@router.put("/{order_item_id}", response_model=OrderItemResponse)
def update_order_item_endpoint(order_item_id: int, order_item: OrderItemUpdate, db: Session = Depends(get_db)):
    return update_order_item(db, order_item_id, order_item)

@router.delete("/{order_item_id}", response_model=OrderItemResponse)
def delete_order_item_endpoint(order_item_id: int, db: Session = Depends(get_db)):
    return delete_order_item(db, order_item_id)