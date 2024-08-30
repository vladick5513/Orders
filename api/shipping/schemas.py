from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShippingBase(BaseModel):
    order_id: int
    address: str
    shipping_date: datetime

class ShippingCreate(ShippingBase):
    pass

class ShippingUpdate(ShippingBase):
    pass

class ShippingResponse(ShippingBase):
    id: int