from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models import Customers
from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str
class CustomerUpdate(BaseModel):
    name: str = None
    email: str = None
    phone: str = None
    address: str = None

def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customers(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer.id

def read_customer(db: Session, customer_id:int):
    customer = db.query(Customers).filter(Customers.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

def update_customer(db: Session, customer_id:int, customer: CustomerUpdate):
    db_customer = db.query(Customers).filter(Customers.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(Customers).filter(Customers.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"ok": True}