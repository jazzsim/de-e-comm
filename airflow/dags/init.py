import os
import datetime
import logging

from pandas import DataFrame
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task, task_group
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.trigger_rule import TriggerRule

logging.basicConfig(level=logging.INFO)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
}

@dag(default_args=default_args, tags=['Initialization'], schedule="@once")
def initialize_warehouse_db():
    @task
    def purge():
        pg_hook = PostgresHook(postgres_conn_id='warehouse_db')
        try:
            pg_hook.run("TRUNCATE TABLE dim_date, dim_customer, dim_address, dim_category, dim_product, dim_customer_support, fact_sales, fact_payments, fact_order_details, fact_cart CASCADE", autocommit=True)

        except Exception as e:
            logging.error(e)
            logging.info("No data to purge")
        
    @task(trigger_rule=TriggerRule.ALL_DONE)
    def create_tables():
        pg_hook = PostgresHook(postgres_conn_id='warehouse_db')
        
        try:
            with open('/opt/airflow/dags/sql/initialize_warehouse_db.sql', 'r') as f:
                sql = f.read()
            pg_hook.run(sql, autocommit=True)
        except Exception as e:
            logging.error(e)
            logging.info("Tables already exist")

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def extract(filename: str):
        dags_folder = os.getenv('AIRFLOW__CORE__DAGS_FOLDER', '/opt/airflow/dags')
        sql_file_path = os.path.join(dags_folder, 'sql', 'extract', filename)
        
        pg_hook = PostgresHook(postgres_conn_id='source_db')
        with open(sql_file_path, 'r') as f:
            sql = f.read()
        df = pg_hook.get_pandas_df(sql)
        logging.info(f"Extracted {len(df)} rows from source database")
        return df
    
    @task
    def transform(df: DataFrame, columns: list[str]):
        # remove columns
        df = df.drop(columns=columns)
        return df
    
    @task
    def load(table_name: str, df: DataFrame):
        pg_hook = PostgresHook(postgres_conn_id='warehouse_db')
        records =[ tuple(row) for row in df.itertuples(index=False, name=None)]
        pg_hook.insert_rows(table= table_name, rows=records)
    
    @task_group(group_id='dim_customer')
    def initDimCustomer():
        df = extract('customers.sql')
        df = transform(df, ['created_at', 'updated_at'])
        load('dim_customer', df)
    
    @task_group(group_id='dim_address')
    def initDimAddress():
        df = extract('addresses.sql')
        load('dim_address', df)
        
    @task_group(group_id='dim_category')
    def initDimCategory():
        df = extract('categories.sql')
        load('dim_category', df)
        
    @task_group(group_id='dim_product')
    def initDimProduct():
        df = extract('products.sql')
        df = transform(df, ['stock_quantity', 'created_at', 'updated_at'])
        load('dim_product', df)
        
    @task_group(group_id='dim_customer_support')
    def initDimCustomerSupport():
        df = extract('customer_support.sql')
        load('dim_customer_support', df)
        
    @task()
    def initDimDate():
        pg_hook = PostgresHook(postgres_conn_id='warehouse_db')
        
        with open('/opt/airflow/dags/sql/date.sql', 'r') as f:
            sql = f.read()
        pg_hook.run(sql, autocommit=True)
    
    purge() >> create_tables() >> initDimDate() >> initDimCustomer() >> initDimAddress() >> initDimCategory() >> initDimProduct() >> initDimCustomerSupport()
    
initialize_warehouse_db()