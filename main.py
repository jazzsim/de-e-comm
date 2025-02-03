from auto import add_product_event, checkout_cart
from db import init_db
from sftp import generate_fake_customer_support_data, load_into_db
from random import randrange

def main():
    #### e-commerce DB ####
    init_db()
    add_product_event()
    checkout_cart()

    #### SFTP ####
    generate_fake_customer_support_data('customer_support_data.csv', randrange(30))
    load_into_db()
    ## SFTP ETL logic: ##
    # 1. every day a Customer Support csv will be uploaded to SFTP
    # 2. the csv will contain today's tickets, with various statuses
    # 3. if an old ticket was resolved, it will be in the csv
    # 4. if ticket is not resolved after 7 days, it will be closed

main()