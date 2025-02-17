from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, Enum, Text, DECIMAL, TIMESTAMP, select, func, MetaData, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime, timezone
from faker import Faker
from decimal import Decimal
from dotenv import load_dotenv

import os
import fake_data
import random

load_dotenv()

# Connect to PostgreSQL
DATABASE_URL = os.getenv('DB_URL')
engine = create_engine(DATABASE_URL)

Base = declarative_base()

# Define the database models
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    image_url = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('shopping_carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)

class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(TIMESTAMP, default=func.now())
    order_status = Column(Enum('Pending', 'Completed', 'Canceled', name='order_status'), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    shipping_address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    billing_address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    payment_id = Column(Integer, ForeignKey('payments.id'), nullable=True)

class OrderDetails(Base):
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    is_default_shipping = Column(Boolean, default=False)
    is_default_billing = Column(Boolean, default=False)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    payment_date = Column(TIMESTAMP, default=func.now())
    payment_method = Column(Enum('Credit Card', 'E-Wallet', name='payment_method'), nullable=False)
    payment_status = Column(Enum('Paid', 'Pending', 'Failed', name='payment_status'), nullable=False)
    transaction_id = Column(String(100), unique=True, nullable=True)

class Customer_Support(Base):
    __tablename__ = 'customer_support'
    ticket_id = Column(String(100), primary_key=True, unique=True, nullable=False, name="ticket_id")
    customer_name = Column(String(255), nullable=False, name='customer_name')
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    issue_category = Column(Enum(
        "Billing",
        "Technical Support",
        "Account Management",
        "Product Inquiry",
        "Shipping",
        "Returns and Refunds",
        name="issue_category"
    ), nullable=False)
    issue_description = Column(String(255), nullable=False)
    date_created = Column(String(20), default=datetime.now().date, nullable=False, name='date_created')
    resolution_date = Column(String(20), default=datetime.now().date, nullable=True, name='resolution_date')
    resolution_status = Column(Enum(
        "Resolved", "Pending", "Escalated",
        name="resolution_status"
    ), nullable=False)

def get_session() -> sessionmaker[Session]:
    Session = sessionmaker(bind=engine)
    return Session

def init_db():
    # Create tables
    Base.metadata.create_all(engine)

    # Seed DB
    Session = get_session()
    session = Session()
    stmt = select(Category)
    if (session.execute(stmt).fetchall() == []):
        categories = fake_data.CATEGORIES
        for i in categories:
            category = Category(
                name = i["category"],
                description= i["description"],
            )
            session.add(category)

    session.commit()  # Save categories to the database

    fake = Faker()


    stmt = select(Product)
    if (session.execute(stmt).fetchall() == []):
        current = 0
        products = fake_data.PRODUCTS
        for i in products:
            index = (current // 5) + 1
            
            product = Product(
                name= i["product"],
                description= i["description"],
                price= Decimal(random.random()) * 20,
                stock_quantity=random.randint(20, 200),  # Random stock quantity between 20 and 200
                category_id= index,
                image_url=fake.image_url(),
            )
            session.add(product)
            current += 1
        session.commit()  # Save products to the database


    stmt = select(Customer)
    if (session.execute(stmt).fetchall() == []):
        for _ in range(200):
            customer = Customer(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                email = fake.email(),
                phone = fake.basic_phone_number(),
                password_hash = fake.password(length=18),
                date_of_birth = fake.date_of_birth(),
            )
            session.add(customer)
        session.commit()

    stmt = select(Address)
    if (session.execute(stmt).fetchall() == []):
        for customer_id in range(200):
            address = Address(
                customer_id = customer_id + 1,
                street=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                postal_code=fake.postalcode(),
                country=fake.country(),
                is_default_shipping=True,
                is_default_billing=True,
            )
            session.add(address)
        session.commit()

def purge():
    Session = get_session()
    session = Session()
    # Restart tables
    session.execute(text(f"TRUNCATE TABLE {Payment.__tablename__} CASCADE"))        
    session.execute(text(f"TRUNCATE TABLE {ShoppingCart.__tablename__} CASCADE"))        
    # reset id to 1
    session.execute(text(f"ALTER SEQUENCE {Payment.__tablename__}_id_seq RESTART WITH 1"))
    session.execute(text(f"ALTER SEQUENCE {OrderDetails.__tablename__}_id_seq RESTART WITH 1"))
    session.execute(text(f"ALTER SEQUENCE {CartItem.__tablename__}_id_seq RESTART WITH 1"))
    session.execute(text(f"ALTER SEQUENCE {Sales.__tablename__}_id_seq RESTART WITH 1"))
    session.execute(text(f"ALTER SEQUENCE {ShoppingCart.__tablename__}_id_seq RESTART WITH 1"))
    session.commit()
    session.close()