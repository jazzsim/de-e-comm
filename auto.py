from sqlalchemy import func
from random import getrandbits, random, randint, choice
from db import Address, CartItem, Customer, OrderDetails, Payment, Product, Sales, ShoppingCart, get_session, Session
import kafka_prod
import uuid

def automate():
    Session = get_session()
    session = Session()

    update_cart_event(session)
    checkout_cart(session)
    
    session.close()

def get_random_cust(session: Session):
    count = randint(1, 50)
    return session.query(Customer).order_by(func.random()).limit(count).all()


def get_random_cart(session: Session):
    total_carts = session.query(ShoppingCart).count()
    count = randint(1, int(total_carts/4))
    return session.query(ShoppingCart).order_by(func.random()).limit(count).all()

# trigger every 5 minute
# each customer will be given a chance to add an item to their cart
def update_cart_event(session: Session):
    add_to_cart(session)
    remove_from_cart(session)
    clear_empty_cart(session)

def add_to_cart(session: Session):
    custs = get_random_cust(session)
    for cust in custs:
        if(getrandbits(1)):
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
    max_quantity_allowed = 20
    quantity = randint(1, max_quantity_allowed)
    
    product_id = randint(1, 50)
    product = session.query(Product).filter(Product.id==product_id).first()

    # will restock when < 20
    if product.stock_quantity < 20:
        product.stock_quantity += 200
        session.commit()
    
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
    kafka_prod.add_to_cart_event(product.id, cart.customer_id, quantity)

def remove_from_cart(session: Session):
    carts = get_random_cart(session)
    for cart in carts:
        chance_to_remove = random() <= 0.2
        if(chance_to_remove):
            remove_product_from_cart(cart, session)

def remove_product_from_cart(cart: ShoppingCart, session: Session):
    items = session.query(CartItem).filter(CartItem.cart_id==cart.id).all()
    item_selected = choice(items)
    product = session.query(Product).filter(Product.id==item_selected.product_id).first()
    
    # randomly remove item by quantity (30% to remove the item)
    if random() <= 0.3:
        # Remove the entire item
        product.stock_quantity += item_selected.quantity
        session.delete(item_selected)
    else:
        # Partially remove quantity
        quantity_to_remove = randint(1, item_selected.quantity)
        product.stock_quantity += quantity_to_remove
        
        if quantity_to_remove == item_selected.quantity:
            session.delete(item_selected)
        else:
            item_selected.quantity -= quantity_to_remove
            item_selected.total_price = item_selected.quantity * item_selected.unit_price
    
    session.commit()

def clear_empty_cart(session: Session):
    # get all carts that don't have cartitem
    session.query(ShoppingCart).filter(
        ~session.query(CartItem).filter(CartItem.cart_id == ShoppingCart.id).exists()
    ).delete(synchronize_session=False)

    session.commit()

# 50% of the carts will have a chance to checkout
# each checkout attempt has 10% chance of cancel/fail
def checkout_cart(session: Session):
    carts = get_random_cart(session)

    for cart in carts:
        if(getrandbits(1)):
            sale_order = create_order(cart, session)
            payment = make_payment(sale_order, session)
            update_sales(sale=sale_order, cart=cart, payment=payment, session=session)


def create_order(cart: ShoppingCart, session: Session):
    total_amount = session.query(func.sum(CartItem.total_price)).filter(CartItem.cart_id == cart.id).scalar()

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
    # 35% to fail
    failed = random() <= 0.35
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