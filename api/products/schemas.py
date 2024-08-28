from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    stock_quantity: int

class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: int = None
    stock_quantity: int = None

class ProductResponse(ProductCreate):
    id: int
    pass




