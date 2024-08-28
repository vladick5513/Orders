from pydantic import BaseModel

class OrderCreate(BaseModel):
    customer_id: int
    status: str
    total_amount: float

class OrderUpdate(BaseModel):
    customer_id: int = None
    status: str = None
    total_amount: float = None