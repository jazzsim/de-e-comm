from etl.etl_func import yesterday_date, upsert

# batch update dim
def update_customer_dim():
    from constant import CUSTOMERS_KEYS
    from sqlalchemy import text
    from db.warehouse_db import DimCustomer

    source_table = 'CUSTOMERS'

    sql = text(f"""
               SELECT id, first_name, last_name, email, phone, date_of_birth, created_at, updated_at
               FROM {source_table} t WHERE t.updated_at > '{yesterday_date()}'
    """) 

    upsert(source_table, DimCustomer, sql, CUSTOMERS_KEYS)

def update_address_dim():
    from constant import ADDRESSES_KEYS
    from sqlalchemy import text
    from db.warehouse_db import DimAddress

    source_table = 'ADDRESSES'

    sql = text(f"""
               SELECT * FROM {source_table} t WHERE t.updated_at > '{yesterday_date()}'
    """) 

    upsert(source_table, DimAddress, sql, ADDRESSES_KEYS)

def update_category_dim():
    from constant import CATEGORIES_KEYS
    from sqlalchemy import text
    from db.warehouse_db import DimCategory

    source_table = 'CATEGORIES'

    sql = text(f"""
               SELECT * FROM {source_table} t WHERE t.updated_at > '{yesterday_date()}'
    """) 

    upsert(source_table, DimCategory, sql, CATEGORIES_KEYS)

def update_product_dim():
    from constant import PRODUCTS_KEYS
    from sqlalchemy import text
    from db.warehouse_db import DimProduct

    source_table = 'PRODUCTS'

    sql = text(f"""
               SELECT 
               id, name, description, price, category_id, image_url, created_at, updated_at 
               FROM {source_table} t WHERE t.updated_at > '{yesterday_date()}'
    """) 

    upsert(source_table, DimProduct, sql, PRODUCTS_KEYS)