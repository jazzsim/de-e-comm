from kafka import KafkaProducer
from datetime import datetime, timezone
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

producer = KafkaProducer(bootstrap_servers=os.getenv('KAFKA_SERVER'), value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# dim cart
def create_cart_event(customer_id: int, cart_id: int):
    event = {
        "type": Event.CREATE_CART.name,
        "user_id": customer_id,
        "cart_id": cart_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)

# fact cart activity
# fact product stock
def add_to_cart_event(product_id: int, customer_id: int, quantity: int):
    event = {
        "type": Event.ADD_TO_CART.name,
        "user_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)

# fact sales
def create_sales_event(cart_id: int, sale_id: int):
    event = {
        "type": Event.CREATE_ORDER.name,
        "cart_id": cart_id,
        "sale_id": sale_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)

# fact payment
def make_payment_event(sale_id: int, payment_method: str, payment_status: str):
    event = {
        "type": Event.MAKE_PAYMENT.name,
        "sale_id": sale_id,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)
    

# fact order details
def success_sale_event(sale_id: int):
    event = {
        "type": Event.SUCCESS_SALE.name,
        "sale_id": sale_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }