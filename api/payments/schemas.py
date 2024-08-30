from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_date: datetime

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int