from db.warehouse_db import init_db
from etl.update_dag import update_customer_dim

def main():
    init_db()
    update_customer_dim()

main()