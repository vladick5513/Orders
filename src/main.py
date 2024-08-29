from fastapi import FastAPI


from api.products.views import router as products_router
from api.customers.views import router as customers_router
from api.orders.views import router as orders_router
from api.order_items.views import router as order_items_router
from api.payments.views import router as payment_router
from api.shipping.views import router as shipping_router

app = FastAPI()
app.include_router(products_router)
app.include_router(customers_router)
app.include_router(orders_router)
app.include_router(order_items_router)
app.include_router(payment_router)
app.include_router(shipping_router)







