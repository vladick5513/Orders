from api.products.schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import Product


async def read_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

async def read_all_products(db: AsyncSession):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products


async def read_products_by_price_range(db: AsyncSession, min_price: int, max_price: int):
    result = await db.execute(select(Product).filter(Product.price.between(min_price, max_price)))
    products = result.scalars().all()
    if not products:
        raise HTTPException(status_code=404, detail=f"No products found in the price range {min_price} - {max_price}")
    return products

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, product_id: int, product: ProductUpdate):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(db_product)
    await db.commit()
    return db_product