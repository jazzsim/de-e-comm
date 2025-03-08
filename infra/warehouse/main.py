# import schedule
from sqlalchemy import text
from kafka import KafkaConsumer
from db import get_session
from enum import Enum
from dotenv import load_dotenv

import logging
import json
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()

class Event(Enum):
    CREATE_CART = "create_cart_event"
    ADD_TO_CART = "add_to_cart_event"
    SALES = "sales_event"
    MAKE_PAYMENT = "make_payment_event"
    SUCCESS_SALE = "success_sale_event"
    ORDER_DETAILS = "order_details_event"


consumer = KafkaConsumer(
    'store-topic',
    bootstrap_servers=os.getenv('KAFKA_SERVER'),
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def listen(event):
    if event['type'] == Event.CREATE_CART.name:
        create_cart_event(event)
    elif event['type'] == Event.ADD_TO_CART.name:
        add_to_cart_event(event)
    elif event['type'] == Event.SALES.name:
        sales_event(event)
    elif event['type'] == Event.MAKE_PAYMENT.name:
        make_payment_event(event)
    elif event['type'] == Event.SUCCESS_SALE.name:
        successful_sales_event(event)
    elif event['type'] == Event.ORDER_DETAILS.name:
        order_details_event(event)
    else:
        logging.info("Unknown event type")

def create_cart_event(data: dict):
    logging.info(f"Create cart event {data}")
    params = {
        "customer_id": data["user_id"],
        "cart_id": data["cart_id"]
    }
    execute_sql_file("sql/dim_cart.sql", params)

def add_to_cart_event(data: dict):
    logging.info(f"Add to cart event {data}")
    product_data = {
        "cart_id": data["cart_id"],
        "product_id": data["product_id"],
        "quantity": data["quantity"],
    }
    execute_sql_file("sql/fact_cart_activity.sql", product_data)
    
def sales_event(data : dict):
    logging.info(f"Sales event {data}")
    sales_data = {
        "total_amount": float(data["total_amount"]),
        "order_status": data["order_status"],
        "customer_id": data["customer_id"],
    }
    execute_sql_file("sql/fact_sales.sql", sales_data)
    
def make_payment_event(data: dict):
    logging.info(f"Make payment event {data}")
    payment_data = {
        "sale_id": data["sale_id"],
        "payment_method": data["payment_method"],
        "payment_status": data["payment_status"],
        "transaction_id": data["transaction_id"],
    }
    execute_sql_file("sql/fact_payments.sql", payment_data)
    
# only save completed sales order_details
def successful_sales_event(data: dict):
    logging.info(f"Successful sales event {data}")
    # update dim_cart table
    close_sale_data = {
        "sale_id": data["sale_id"],
        "transaction_id": data["transaction_id"]
    }
    execute_sql_file("sql/close_sale.sql", close_sale_data)

# only save completed sales order_details
def order_details_event(data: dict):
    logging.info(f"Order details event {data}")
    order_data = {
        "sale_id": data["sale_id"],
        "product_id": data["product_id"],
        "quantity": data["quantity"],
        "total_price": float(data["total_price"])
    }
    execute_sql_file("sql/fact_order_details.sql", order_data)

def execute_sql_file(file_path: str, data: dict = None):
    Session = get_session()
    session = Session()
    with open(file_path, "r") as file:
        query = file.read()
    session.execute(text(query), data)
    session.commit()
    session.close()

# Process messages
for msg in consumer:
    listen(msg.value)