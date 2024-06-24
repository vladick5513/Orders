from models import Customers, Product, Order, OrderItem, Payment, Shipping
from database import sync_engine, session_factory, Base
from datetime import datetime, timedelta

def create_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)

def insert_data():
    with session_factory() as session:
        customer1 = Customers(name="John Doe", email="john.doe@example.com", phone="123-456-7890",
                              address="123 Main St")
        customer2 = Customers(name="Jane Smith", email="jane.smith@example.com", phone="987-654-3210",
                              address="456 Elm St")

        product1 = Product(name="Laptop", description="A powerful laptop", price=1500.00, stock_quantity=10)
        product2 = Product(name="Smartphone", description="A feature-rich smartphone", price=800.00, stock_quantity=25)

        order1 = Order(customer=customer1, status="Delivered", total_amount=1500.00)
        order2 = Order(customer=customer2, status="Shipped", total_amount=1600.00)

        order_item1 = OrderItem(order=order1, product=product1, quantity=1, price=1500.00, total_price=1500.00)
        order_item2 = OrderItem(order=order2, product=product2, quantity=2, price=800.00, total_price=1600.00)

        payment1 = Payment(order=order1, amount=1500.00, payment_method="Credit Card")
        payment2 = Payment(order=order2, amount=1600.00, payment_method="PayPal")

        shipping1 = Shipping(order=order1, shipping_address="123 Main St", shipping_date=datetime.now(),
                             delivery_date=datetime.now() + timedelta(days=1), status="Delivered")
        shipping2 = Shipping(order=order2, shipping_address="456 Elm St",
                             shipping_date=datetime.now() + timedelta(days=1),
                             delivery_date=datetime.now() + timedelta(days=2), status="Shipped")

        session.add_all(
            [customer1, customer2,
             product1, product2,
             order1, order2,
             order_item1, order_item2, payment1,
             payment2,
             shipping1, shipping2])
        session.commit()










