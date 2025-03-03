from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from faker import Faker
from decimal import Decimal
from dotenv import load_dotenv

import os
import random

load_dotenv()

# Connect to PostgreSQL
DATABASE_URL = os.getenv('DB_URL')
engine = create_engine(DATABASE_URL)

Base = declarative_base()

def get_session() -> sessionmaker[Session]:
    Session = sessionmaker(bind=engine)
    return Session

def init_db():
    # Create tables
    Base.metadata.create_all(engine)

    # Seed DB
    Session = get_session()
    session = Session()

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