import csv
import random
import datetime

from faker import Faker
from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker
from db import Customer, Customer_Support

Base = declarative_base()
# Connect to PostgreSQL
DATABASE_URL = "postgresql://localhost:5432/ecommerce_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def generate_fake_customer_support_data(output_file, num_records):
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

def load_into_db():
    # load csv
    import pandas as pd

    # Step 1: Read CSV file into a pandas DataFrame
    csv_file = 'customer_support_data.csv'
    df = pd.read_csv(csv_file)

    # clear dups
    df = df.drop_duplicates()

    # Ticket system bug: sometimes status doesn't get updated from pending to completed
    df.loc[(df['Resolution Status'] == 'Pending') & (df['Resolution Date'].notna()), 'Resolution Status'] = "Resolved"

    # rename columns
    df.columns = df.columns.str.replace(' ', '_').str.lower()

    df.to_sql('customer_support', engine, if_exists='append', index=False)


    print("CSV data has been loaded to PostgreSQL successfully.")

def load_previous_unresolve(writer):
    # load existing non-resolved tickets and add into new sheet
    unresovled = session.query(Customer_Support).filter(Customer_Support.resolution_status.not_like('Resolved')).all()
    for un in unresovled:
        # randomly update status
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
        
