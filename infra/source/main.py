from auto import automate
from db import init_db, purge
from ftp import generate_customer_support_data, delete_prev, upload
from random import randrange
from datetime import datetime
from kafka_prod import create_cart_event

import time
import schedule

def generate_csv():
    current_date = datetime.now().strftime('%Y-%m-%d')
    count = randrange(30)
    generate_customer_support_data(f'customer_support_data_{current_date}.csv', count)
    # delete old csv
    delete_prev()
    # upload to ftp
    upload()

def main():

    create_cart_event(43, 18);

    # # Schedule tasks
    # schedule.every(5).seconds.do(automate)
    # schedule.every().day.at("00:00").do(generate_csv)  # Run once per day at midnight
    schedule.every(25).days.do(purge)
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent CPU overuse

    ## FTP ETL logic: ##
    # 1. every day a Customer Support csv will be uploaded to FTP
    # 2. the csv will contain today's tickets, with various statuses
    # 3. if an old ticket was resolved, it will be in the csv
    # 4. if ticket is not resolved after 7 days, it will be closed
    # load_into_db()

init_db()
main()