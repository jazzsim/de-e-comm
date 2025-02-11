import csv
import random
import datetime

from ftplib import FTP_TLS
from faker import Faker
from sqlalchemy import select, func
from db import session, engine, Customer, Customer_Support
from dotenv import load_dotenv

import os

load_dotenv()

def generate_customer_support_data(output_file, num_records):
    # Initialize Faker and define categories for issues
    fake = Faker()
    issue_categories = [
        "Billing",
        "Technical Support",
        "Account Management",
        "Product Inquiry",
        "Shipping",
        "Returns and Refunds"
    ]
    resolutions = ["Resolved", "Pending", "Escalated"]


    # Open the file for writing
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow([
            "Ticket ID",
            "Customer Name",
            "Email",
            "Phone",
            "Issue Category",
            "Issue Description",
            "Date Created",
            "Resolution Status",
            "Resolution Date"
        ])

        load_previous_unresolve(writer)

        # get all customers from db
        stmt = select(Customer)
        customers = session.execute(stmt).fetchall()

        # Generate fake data for each record
        for _ in range(num_records):
            customer = random.choice(customers)[0]
            ticket_id = fake.uuid4()
            customer_name = customer.first_name + " " + customer.last_name
            email = customer.email
            phone = customer.phone
            issue_category = random.choice(issue_categories)
            issue_description = fake.sentence(nb_words=10)
            date_created = datetime.date.today()
            resolution_status = random.choice(resolutions)
            resolution_date = (
                date_created if resolution_status == "Resolved" else ""
            )

            # Simulate delayed ticket resolution updates
            if resolution_status == "Resolved" and random.random() > 0.2:
                resolution_status = "Pending"  # Mark as pending despite being resolved

            # Simulate duplicate rows
            if random.random() > 0.85:
                writer.writerow([
                    ticket_id,
                    customer_name,
                    email,
                    phone,
                    issue_category,
                    issue_description,
                    date_created,
                    resolution_status,
                    resolution_date
                ])

            # Write the row to the CSV file
            writer.writerow([
                ticket_id,
                customer_name,
                email,
                phone,
                issue_category,
                issue_description,
                date_created,
                resolution_status,
                resolution_date
            ])

def load_previous_unresolve(writer):
    # load existing non-resolved tickets and add into new sheet
    if session.query(Customer_Support).first() != None:
        unresovled = session.query(Customer_Support).filter(Customer_Support.resolution_status != 'Resolved').all()
        for un in unresovled:
            # randomly update status (mock)
            if (random.getrandbits(1)):
                writer.writerow([
                    un.ticket_id,
                    un.customer_name,
                    un.email,
                    un.phone,
                    un.issue_category,
                    un.issue_description,
                    un.date_created,
                    "Resolved",
                    datetime.date.today()
                ])

def delete_prev():
    yesterday = (datetime.today() - datetime.timedelta(days = 0)).strftime('%Y-%m-%d')
    
    prev = f'customer_support_data_{yesterday}.csv'
    # If file exists, delete it.
    if os.path.isfile(prev):
        os.remove(prev)
    else:
        # If it fails, inform the user.
        print("Error: %s file not found" % prev)
            
def upload():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'customer_support_data_{current_date}.csv'

    # FTP server details
    hostname = os.getenv('FTP_SERVER_HOSTNAME')
    username = os.getenv('FTP_SERVER_USERNAME')
    password = os.getenv('FTP_SERVER_PASSWORD')
    local_file_path =  filename
    remote_file_path = f'{os.getenv('FTP_SERVER_REMOTE_FILE_PATH')}{filename}'

    # Connect to FTP server
    ftps = FTP_TLS(hostname)

    try:
        # Login to the server
        ftps.login(username, password)

        ftps.prot_p()
        
        # Open the local file
        with open(local_file_path, 'rb') as file:
            # Upload the file using STOR command
            ftps.storbinary(f"STOR {remote_file_path}", file)
            print(f"File successfully uploaded to {remote_file_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Quit the FTP session
        ftps.quit()



# ETL
def load_into_db():
    # load csv
    import pandas as pd


    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # Step 1: Read CSV file into a pandas DataFrame
    csv_file = f'customer_support_data_{current_date}.csv'
    df = pd.read_csv(csv_file)

    # clear dups
    df = df.drop_duplicates()

    # Ticket system bug: sometimes status doesn't get updated from pending to completed
    df.loc[(df['Resolution Status'] == 'Pending') & (df['Resolution Date'].notna()), 'Resolution Status'] = "Resolved"

    # rename columns
    df.columns = df.columns.str.replace(' ', '_').str.lower()

    # TODO: update tickets status
    # 

    df.to_sql('customer_support', engine, if_exists='append', index=False)


    print("CSV data has been loaded to PostgreSQL successfully.")
