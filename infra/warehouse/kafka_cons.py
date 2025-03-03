from sqlalchemy import text
from kafka import KafkaConsumer
from db import get_session, Session
from enum import Enum
from dotenv import load_dotenv

import json
import os

load_dotenv()

class Event(Enum):
    CREATE_CART = "create_cart_event"
    ADD_TO_CART = "add_to_cart_event"
    SALES = "sales_event"
    MAKE_PAYMENT = "make_payment_event"
    SUCCESS_SALE = "success_sale_event"


producer = KafkaConsumer(
    'store-topic',
    bootstrap_servers=os.getenv('KAFKA_SERVER'),
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def add_to_cart_event():
    for message in producer:
        event = message.value

        if event['type'] == Event.CREATE_CART.name:
            print(event['user_id'], event['cart_id'], event['timestamp'])
            create_cart_event(event)
        elif event['type'] == Event.ADD_TO_CART.name:
            print(event['user_id'], event['product_id'], event['quantity'], event['timestamp'])
            add_to_cart_event(event)
        elif event['type'] == Event.SALES.name:
            print(event['cart_id'], event['sale_id'], event['timestamp'])
            sales_event(event)
        elif event['type'] == Event.MAKE_PAYMENT.name:
            print(event['sale_id'], event['payment_method'], event['payment_status'], event['timestamp'])
            make_payment_event(event)
        elif event['type'] == Event.SUCCESS_SALE.name:
            print(event['sale_id'], event['timestamp'])
            successful_sales_event(event)
        else:
            print("Unknown event type")

def create_cart_event(data: dict):
    execute_sql_file("sql/dim_cart.sql", data)

def add_to_cart_event(data: dict):
    execute_sql_file("sql/fact_cart_activity.sql", data)
    product_data = {
        "product_id": data["product_id"],
        "quantity": data["quantity"]
    }
    execute_sql_file("sql/fact_product_stock.sql", product_data)
    
def sales_event(data : dict):
    execute_sql_file("sql/fact_sales.sql", data)
    
def make_payment_event(data: dict):
    execute_sql_file("sql/fact_payment.sql", data)
    
# only save completed sales order_details
def successful_sales_event(data: dict):
    execute_sql_file("sql/fact_order_details.sql", data)

def execute_sql_file(file_path: str, data: dict = None):
    session = get_session()
    session = Session()
    with open(file_path, "r") as file:
        query = text(file.read())
        session.execute(query, data)
    session.close()