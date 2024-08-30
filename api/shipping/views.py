from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.shipping.crud import create_shipping, read_shipping, update_shipping, delete_shipping
from api.shipping.schemas import ShippingCreate, ShippingUpdate, ShippingResponse
from src.database import get_db

router = APIRouter(prefix="/shipping", tags=["Shipping"])

@router.post("/", response_model=ShippingResponse)
def create_shipping_endpoint(shipping: ShippingCreate, db: Session = Depends(get_db)):
    return create_shipping(db, shipping)

@router.get("/{shipping_id}", response_model=ShippingResponse)
def read_shipping_endpoint(shipping_id: int, db: Session = Depends(get_db)):
    return read_shipping(db, shipping_id)

@router.put("/{shipping_id}", response_model=ShippingResponse)
def update_shipping_endpoint(shipping_id: int, shipping: ShippingUpdate, db: Session = Depends(get_db)):
    return update_shipping(db, shipping_id, shipping)

@router.delete("/{shipping_id}", response_model=ShippingResponse)
def delete_shipping_endpoint(shipping_id: int, db: Session = Depends(get_db)):
    return delete_shipping(db, shipping_id)