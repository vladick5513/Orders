from pydantic import BaseModel


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    pass

