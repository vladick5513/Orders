from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from fastapi_users.db import SQLAlchemyBaseUserTable

class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class Customers(Base):
    __tablename__ = "customers"
    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, unique=True, index=True)
    phone = mapped_column(String)
    address = mapped_column(Text)
    created_at = mapped_column(DateTime, server_default=func.now())

    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    description = mapped_column(Text)
    price = mapped_column(Float, nullable= False )
    stock_quantity = mapped_column(Integer, nullable=False )
    created_at = mapped_column(DateTime, server_default=func.now())

class Order(Base):
    __tablename__ = "orders"
    id = mapped_column(Integer, primary_key=True, index=True)
    customer_id = mapped_column(Integer, ForeignKey('customers.id'))
    orders_date = mapped_column(DateTime, server_default=func.now())
    status = mapped_column(String, nullable=False)
    total_amount = mapped_column(Float, nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now())

    customer = relationship("Customers", back_populates="orders")
    order_items = relationship("OrderItem",  back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = mapped_column(Integer, primary_key=True, index=True)
    order_id = mapped_column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    price = mapped_column(Float, nullable=False)
    total_price = mapped_column(Float, nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now())

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")

class Payment(Base):
    __tablename__ = "payments"
    id = mapped_column(Integer, primary_key=True, index=True)
    order_id = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_date = mapped_column(DateTime, server_default=func.now())
    amount = mapped_column(Float, nullable=False)
    payment_method = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now())

    order = relationship("Order")

class Shipping(Base):
    __tablename__ = "shipping"
    id = mapped_column(Integer, primary_key=True, index=True)
    order_id = mapped_column(Integer, ForeignKey("orders.id"))
    shipping_address = mapped_column(Text, nullable=False)
    shipping_date = mapped_column(DateTime)
    delivery_date = mapped_column(DateTime)
    status = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now())

    order = relationship("Order")






