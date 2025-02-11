from typing import List
from sqlalchemy import func
from random import randrange, sample, getrandbits, random, randint
from db import session, Address, CartItem, Customer, OrderDetails, Payment, Product, Sales, ShoppingCart
from math import ceil
import kafka_prod
import uuid

def automate():
    add_product_event()
    checkout_cart()

# trigger every 5 minute
# each customer will be given a chance to add an item to their cart
def add_product_event():
    number_of_cust_to_choose = randrange(10)
    # get x number of customer
    customers = sample(range(1,21), number_of_cust_to_choose)
    # run query to get all cust
    custs = session.query(Customer).filter(Customer.id.in_((customers))).all()
    add_to_cart(custs)

def add_to_cart(custs: List[Customer]):
    for cust in custs:
        if(getrandbits(1)):
            print(f"custs id = {cust.id}")
            cart = get_cart(cust.id)
            add_product_to_cart(cart)
            
def get_cart(id: int):
    cart = session.query(ShoppingCart).filter_by(customer_id=id).first()
    if not cart:
        cart = ShoppingCart(customer_id=id)
        session.add(cart)
        session.commit()
    return cart

def add_product_to_cart(cart: ShoppingCart):
    product_id = randrange(50)
    product = session.query(Product).filter_by(id=product_id).first()
    quantity = randint(1, product.stock_quantity)
    if (quantity > 20):
        quantity = 20

    cart_item = session.query(CartItem).filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
        cart_item.total_price = cart_item.quantity * cart_item.unit_price
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=product.price,
            total_price=quantity * product.price
        )
        session.add(cart_item)
    session.commit()

    product.stock_quantity -= quantity
    session.commit()
    kafka_prod.add_to_cart_event(product.id, cart.customer_id, quantity)

# 50% of the carts will have a chance to checkout
# each checkout attempt has 10% chance of cancel/fail
def checkout_cart():
    # select all cart
    amount_of_carts = session.query(ShoppingCart).count()

    forty_percent_of_carts = ceil(amount_of_carts / 2)

    carts = sample(range(1, amount_of_carts + 1), forty_percent_of_carts)

    data = session.query(ShoppingCart).filter(ShoppingCart.id.in_((carts))).all()

    for cart in data:
        if(getrandbits(1)):
            sale_order = create_order(cart)
            payment = make_payment(sale_order)
            update_sales(sale=sale_order, cart=cart, payment=payment)


def create_order(cart: ShoppingCart):
    total_amount = session.query(func.sum(CartItem.total_price)).filter_by(cart_id=cart.id).scalar()

    address = session.query(Address).filter(Address.customer_id == cart.customer_id).scalar()

    sale = Sales(
        customer_id=cart.customer_id,
        order_status="Pending",
        total_amount=total_amount,
        shipping_address_id=address.id,
        billing_address_id=address.id
    )
    session.add(sale)
    session.commit()
    create_order_detail(cart=cart, sale=sale)
    kafka_prod.create_order_event(cart.id, sale.id)
    return sale

def create_order_detail(cart: ShoppingCart, sale: Sales):
    cart_items = session.query(CartItem).filter_by(cart_id=cart.id).all()

    for item in cart_items:
        order_detail = OrderDetails(
            order_id=sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.total_price
        )
        session.add(order_detail)
    session.commit()

def make_payment(sale: Sales):
    # 10% to fail
    failed = random() <= 0.1
    payment_status = "Paid"
    if(failed):
        payment_status = "Failed"

    # randomize method
    alter_method = random() <= 0.5
    payment_method = "Credit Card"
    if(alter_method):
        payment_method = "E-Wallet"

    payment = Payment(
        order_id=sale.id,
        payment_method=payment_method,
        payment_status=payment_status,
        transaction_id=uuid.uuid4()  # Custom function to generate a unique ID
    )
    session.add(payment)
    session.commit()
    kafka_prod.make_payment_event(sale.id, payment_method, payment_status)
    return payment

def update_sales(sale : Sales, cart: ShoppingCart, payment: Payment):
    if(payment.payment_status != "Paid"):
        sale.order_status = "Canceled"
    else:
        sale.order_status = "Completed"
        sale.payment_id = payment.id
        session.query(CartItem).filter_by(cart_id=cart.id).delete()
        session.query(ShoppingCart).filter_by(id=cart.id).delete()
    session.commit()