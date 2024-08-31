from pydantic import BaseModel
from datetime import datetime


class ShippingBase(BaseModel):
    order_id: int
    shipping_address: str
    shipping_date: datetime
    delivery_date: datetime
    status: str

class ShippingCreate(ShippingBase):
    pass

class ShippingUpdate(ShippingBase):
    pass

class ShippingResponse(ShippingBase):
    id: int
    pass