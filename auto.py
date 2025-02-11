from typing import List
from sqlalchemy import func, update
from random import randrange, sample, getrandbits, random, randint, choice
from db import Address, CartItem, Customer, OrderDetails, Payment, Product, Sales, ShoppingCart, get_session, Session
from math import ceil
import kafka_prod
import uuid

def automate():
    Session = get_session()
    session = Session()

    update_cart_event(session)
    checkout_cart(session)
    
    session.close()

def get_random_cust(session: Session):
    number_of_cust_to_choose = randrange(100)
    # get x number of customer
    customers = sample(range(1,201), number_of_cust_to_choose)
    # run query to get all cust
    return session.query(Customer).filter(Customer.id.in_((customers))).all()


def get_random_cart(session: Session):
    total_carts = session.query(ShoppingCart).count()
    number_of_cart_to_choose = randrange(total_carts)
    # get x number of cart
    carts = sample(range(1, total_carts), number_of_cart_to_choose)
    # run query to get all cart
    return session.query(ShoppingCart).filter(ShoppingCart.id.in_((carts))).all()

# trigger every 5 minute
# each customer will be given a chance to add an item to their cart
def update_cart_event(session: Session):
    add_to_cart(session)
    remove_from_cart(session)

def add_to_cart(session: Session):
    custs = get_random_cust(session)
    for cust in custs:
        if(getrandbits(1)):
            print(f"custs id = {cust.id}")
            cart = get_cart(id=cust.id, session=session)
            add_product_to_cart(cart, session)
            
def get_cart(id: int ,session: Session, create : bool = True ):
    cart = session.query(ShoppingCart).filter(ShoppingCart.customer_id==id).first()
    if not cart and create:
        cart = ShoppingCart(customer_id=id)
        session.add(cart)
        session.commit()
    return cart

def add_product_to_cart(cart: ShoppingCart, session: Session):
    print('add')
    max_quantity_allowed = 20
    quantity = randint(1, max_quantity_allowed)
    
    product_id = randint(1, 50)
    product = session.query(Product).filter(Product.id==product_id).first()
    print(f'product {product}')

    # will restock when < 20
    if product.stock_quantity < 20:
        stmt = (update(Product).where(Product.c.id == product.id).values(stock_quantity = 100))
        session.execute(stmt)

    # # discard if out of stock
    # if quantity > product.stock_quantity:
    #     cart_item = session.query(CartItem).filter(CartItem.cart_id==cart.id).first()
    #     if cart_item is None:
    #         session.delete(cart)
    #         # emit delete cart event
    #         session.commit()
    #     return
    
    print('conn')

    cart_item = session.query(CartItem).filter(CartItem.cart_id==cart.id, CartItem.product_id==product_id).first()
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

    product.stock_quantity -= quantity
    session.commit()
    print('commited')
    kafka_prod.add_to_cart_event(product.id, cart.customer_id, quantity)

def remove_from_cart(session: Session):
    carts = get_random_cart(session)
    for cart in carts:
        chance_to_remove = random() <= 0.4
        if(chance_to_remove):
            remove_product_from_cart(cart, session)
    # custs = get_random_cust(session)
    # for cust in custs:
    #     if(getrandbits(1)):
    #         print(f"removed custs id = {cust.id}")
    #         cart = get_cart(id=cust.id, create=False, session=session)
    #         if cart:
    #             remove_product_from_cart(cart, session)

def remove_product_from_cart(cart: ShoppingCart, session: Session):
    items = session.query(CartItem).filter(CartItem.cart_id==cart.id).all()
    # randomly remove item by quantity (40% to remove the item)
    item_selected = choice(items)
    remove_item = random() <= 0.4
    if remove_item:
        session.delete(item_selected)
        print('remove item')
    else:
        quantity_to_be_remove = randint(1, item_selected.quantity)
        if quantity_to_be_remove == item_selected.quantity:
            session.delete(item_selected)
        else :
            item_selected.quantity -= quantity_to_be_remove
            item_selected.total_price = item_selected.quantity * item_selected.unit_price
        print('remove item by quantity')
    clear_empty_cart(cart=cart, session=session)
    session.commit()

def clear_empty_cart(cart: ShoppingCart, session: Session):
    count = session.query(CartItem).filter(CartItem.cart_id==cart.id).count()
    print(f'count {count}')
    if count == 0:
        session.delete(cart);
        session.commit()

# 50% of the carts will have a chance to checkout
# each checkout attempt has 10% chance of cancel/fail
def checkout_cart(session: Session):
    # select all cart
    amount_of_carts = session.query(ShoppingCart).count()

    forty_percent_of_carts = ceil(amount_of_carts / 2)

    carts = sample(range(1, amount_of_carts + 1), forty_percent_of_carts)

    data = session.query(ShoppingCart).filter(ShoppingCart.id.in_((carts))).all()

    for cart in data:
        if(getrandbits(1)):
            sale_order = create_order(cart, session)
            payment = make_payment(sale_order, session)
            update_sales(sale=sale_order, cart=cart, payment=payment, session=session)


def create_order(cart: ShoppingCart, session: Session):
    total_amount = session.query(func.sum(CartItem.total_price)).filter(CartItem.cart_id == cart.id).scalar()
    print(f'cart = {cart.id}')
    print(f'total = {total_amount}')

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
    create_order_detail(cart=cart, sale=sale, session=session)
    kafka_prod.create_order_event(cart.id, sale.id)
    return sale

def create_order_detail(cart: ShoppingCart, sale: Sales, session: Session):
    cart_items = session.query(CartItem).filter(CartItem.cart_id==cart.id).all()

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

def make_payment(sale: Sales, session: Session):
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

def update_sales(sale : Sales, cart: ShoppingCart, payment: Payment, session: Session):
    if(payment.payment_status != "Paid"):
        sale.order_status = "Canceled"
    else:
        sale.order_status = "Completed"
        sale.payment_id = payment.id
        session.query(CartItem).filter(CartItem.cart_id==cart.id).delete()
        session.query(ShoppingCart).filter(ShoppingCart.id==cart.id).delete()
    session.commit()