from fastapi import FastAPI


from api.products.views import router as products_router
from api.customers.views import router as customers_router
from api.orders.views import router as orders_router

app = FastAPI()
app.include_router(products_router)
app.include_router(customers_router)
app.include_router(orders_router)







