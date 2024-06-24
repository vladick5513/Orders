from models import Customers, Product, Order, OrderItem, Payment, Shipping
from database import sync_engine, session_factory, Base

def create_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)

