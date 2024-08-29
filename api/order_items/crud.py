from api.order_items.schemas import OrderItemCreate, OrderItemUpdate
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models import OrderItem


def create_order_item(db: Session, order_item: OrderItemCreate):
    db_order_items = OrderItem(**order_item.model_dump())
    db.add(db_order_items)
    db.commit()
    db.refresh(db_order_items)
    return db_order_items.id

def read_order_item(db: Session, order_item_id: int):
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if order_item is None:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    return order_item

def update_order_item(db: Session, order_item_id: int, order_item: OrderItemUpdate):
    db_order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if db_order_items is None:
        raise HTTPException(status_code=404, detail="OrderItem")
    for key, value in order_item.model_dump(exclude_unset=True).items():
        setattr(db_order_items, key, value)
        db.commit()
        db.refresh(db_order_items)
        return db_order_item

def delete_order_item(db: Session, order_item_id: int):
    db_order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if db_order_item is None:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    db.delete(db_order_item)
    db.commit()
    return {"ok": True}
