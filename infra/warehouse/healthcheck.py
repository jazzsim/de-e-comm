from warehouse.db.warehouse_db import get_session, Session, FactSales
def check_db_connection():
    try:
        session = get_session()
        session = Session()
        session.query(FactSales).first()
        session.close()
        return True
    except Exception as _:
        return False

if __name__ == "__main__":
    print("Warehouse database is healthy" if check_db_connection() else "Warehouse database connection failed")