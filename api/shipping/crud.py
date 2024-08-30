from sqlalchemy.orm import Session
from api.shipping.schemas  import ShippingCreate, ShippingUpdate
from src.models import Shipping

def create_shipping(db: Session, shipping: ShippingCreate):
    db_shipping = Shipping(**shipping.dict())
    db.add(db_shipping)
    db.commit()
    db.refresh(db_shipping)
    return db_shipping

def read_shipping(db: Session, shipping_id: int):
    return db.query(Shipping).filter(Shipping.id == shipping_id).first()

def update_shipping(db: Session, shipping_id: int, shipping: ShippingUpdate):
    db_shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not db_shipping:
        return None
    for key, value in shipping.dict(exclude_unset=True).items():
        setattr(db_shipping, key, value)
    db.commit()
    db.refresh(db_shipping)
    return db_shipping

def delete_shipping(db: Session, shipping_id: int):
    db_shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if db_shipping:
        db.delete(db_shipping)
        db.commit()
        return True
    return False