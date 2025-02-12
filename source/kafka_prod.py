from kafka import KafkaProducer
from datetime import datetime, timezone
from enum import Enum
from dotenv import load_dotenv

import json
import os

load_dotenv()

class Event(Enum):
    ADD_TO_CART = "add_to_cart_event"
    CREATE_ORDER = "create_order_event"
    MAKE_PAYMENT = "make_payment_event"

producer = KafkaProducer(bootstrap_servers=os.getenv('KAFKA_SERVER'), value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def add_to_cart_event(product_id: int, customer_id: int, quantity: int):
    event = {
        "type": Event.ADD_TO_CART.name,
        "user_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)

def create_order_event(cart_id: int, sale_id: int):
    event = {
        "type": Event.CREATE_ORDER.name,
        "cart_id": cart_id,
        "sale_id": sale_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)

def make_payment_event(sale_id: int, payment_method: str, payment_status: str):
    event = {
        "type": Event.MAKE_PAYMENT.name,
        "sale_id": sale_id,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)