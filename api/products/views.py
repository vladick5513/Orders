from api.products.crud import create_product, read_product, update_product, delete_product
from api.products.schemas import ProductCreate, ProductUpdate, ProductResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db


router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
async def create_product_endpoint(product: ProductCreate,db: AsyncSession = Depends(get_db)):
    return await create_product(db, product)

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product_endpoint(product_id: int, db: AsyncSession = Depends(get_db)):
    return await read_product(db, product_id)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(product_id: int, product:ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await update_product(db, product, product_id)

@router.delete("/{product_id}", response_model=ProductResponse)
async def delete_product_endpoint(product_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_product(db, product_id)