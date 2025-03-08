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
    ORDER_DETAILS = "order_details_event"

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
def add_to_cart_event(cart_id: int, product_id: int, quantity: int):
    event = {
        "type": Event.ADD_TO_CART.name,
        "cart_id": cart_id,
        "product_id": product_id,
        "quantity": quantity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)

# fact sales
def create_sales_event(total_amount: str, order_status: str, customer_id: int):
    event = {
        "type": Event.SALES.name,
        "total_amount": total_amount,
        "order_status": order_status,
        "customer_id": customer_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)

# fact payment
def make_payment_event(sale_id: int, payment_method: str, payment_status: str, transaction_id: str):
    event = {
        "type": Event.MAKE_PAYMENT.name,
        "sale_id": sale_id,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "transaction_id": transaction_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)
    

# fact sales & payments
def success_sale_event(sale_id: int, transaction_id: str):
    event = {
        "type": Event.SUCCESS_SALE.name,
        "sale_id": sale_id,
        "transaction_id": transaction_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)
    
# fact order details
def order_details_event(sale_id: int, product_id: int, quantity: int, total_price: float):
    event = {
        "type": Event.ORDER_DETAILS.name,
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": quantity,
        "total_price": total_price,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    producer.send('store-topic', value=event)