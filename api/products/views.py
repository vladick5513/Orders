from api.products.crud import create_product, read_product, update_product, delete_product
from api.products.schemas import ProductCreate, ProductUpdate, ProductResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db


router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create_product_endpoint(product: ProductCreate,db: Session = Depends(get_db)):
    return create_product(db, product)

@router.get("/{product_id}")
def read_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return read_product(db, product_id)

@router.put("/{product_id}")
def update_product_endpoint(product_id: int, product:ProductUpdate, db: Session = Depends(get_db)):
    return update_product(db, product, product_id)

@router.delete("/{product_id}")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)