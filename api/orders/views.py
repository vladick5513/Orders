from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.orders.crud import create_order, read_order, update_order, delete_order
from src.database import get_db
from api.orders.schemas import OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=int)
def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)

@router.get("/{order_id}")
def read_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    return read_order(db, order_id)

@router.put("/{order_id}")
def update_order_endpoint(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    return update_order(db, order_id, order)

@router.delete("/{order_id}")
def delete_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    return delete_order(db, order_id)