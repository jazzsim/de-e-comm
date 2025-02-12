from db import get_session, Session, Customer
def check_db_connection():
    try:
        session = get_session()
        session = Session()
        session.query(Customer).first()
        session.close()
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    print("E-Commerce database is healthy" if check_db_connection() else "E-Commerce database connection failed")