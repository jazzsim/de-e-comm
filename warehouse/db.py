from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, Enum, Text, DECIMAL, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime, timezone
from dotenv import load_dotenv

import os

load_dotenv()

# Connect to PostgreSQL
DATABASE_URL = os.getenv('WAREHOUSE_DB_URL')
engine = create_engine(DATABASE_URL)

Base = declarative_base()

# Define the database models
class FactSales(Base):
    __tablename__ = 'fact_sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    order_status = Column(Enum('Pending', 'Completed', 'Canceled', name='order_status'), nullable=False)
    order_date_id = Column(Integer, ForeignKey('dim_date.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('dim_customer.id'), nullable=False)
    shipping_address_id = Column(Integer, ForeignKey('dim_address.id'), nullable=False)
    billing_address_id = Column(Integer, ForeignKey('dim_address.id'), nullable=False)
    payment_id = Column(Integer, ForeignKey('fact_payments.id'), nullable=True)

class FactOrderDetails(Base):
    __tablename__ = 'fact_order_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('fact_sales.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('dim_product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)

class FactPayments(Base):
    __tablename__ = 'fact_payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('fact_sales.id'), nullable=False)
    payment_date_id = Column(Integer, ForeignKey('dim_date.id'), nullable=False)
    payment_method = Column(Enum('Credit Card', 'E-Wallet', name='payment_method'), nullable=False)
    payment_status = Column(Enum('Paid', 'Pending', 'Failed', name='payment_status'), nullable=False)
    transaction_id = Column(String(100), unique=True, nullable=True)

# for cart abandoned rate, conversion rate, etc.
class FactCart(Base):
    __tablename__ = 'fact_cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('dim_customer.id'), nullable=False)
    sale_id = Column(Integer, ForeignKey('fact_sales.id'), nullable=True) # exist when user checkout
    cart_created_timestamp = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    cart_updated_timestamp = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class FactProductStock(Base):
    __tablename__ = 'fact_product_stock'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('dim_product.id'), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


# Define the database models
class DimCustomer(Base):
    __tablename__ = 'dim_customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class DimProduct(Base):
    __tablename__ = 'dim_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey('dim_category.id'), nullable=True)
    image_url = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class DimCategory(Base):
    __tablename__ = 'dim_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

class DimAddress(Base):
    __tablename__ = 'dim_address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('dim_customer.id'), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    is_default_shipping = Column(Boolean, default=False)
    is_default_billing = Column(Boolean, default=False)

class Dim_Date(Base):
    __tablename__ = 'dim_date'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_date = Column(String(20), nullable=False, name='full_date')
    quarter = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    week_of_year = Column(Integer, nullable=False, name='week_of_year')
    day_of_week = Column(String(20), nullable=False, name='day_of_week')

class Dim_Customer_Support(Base):
    __tablename__ = 'dim_customer_support'
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