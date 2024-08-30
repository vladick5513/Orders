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

class CustomerResponse(CustomerCreate):
    id: int
    pass