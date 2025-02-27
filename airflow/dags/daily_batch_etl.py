import os
import logging

from pandas import DataFrame
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task, task_group
from airflow.providers.postgres.hooks.postgres import PostgresHook

logging.basicConfig(level=logging.INFO)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
}

@dag(default_args=default_args, tags=['Batch ETL'], schedule="@daily")
def daily_batch_etl():

    @task
    def transform(df: DataFrame, columns: list[str]):
        # remove columns
        df = df.drop(columns=columns)
        return df

    @task
    def extract(filename: str):
        dags_folder = os.getenv('AIRFLOW__CORE__DAGS_FOLDER', '/opt/airflow/dags')
        sql_file_path = os.path.join(dags_folder, 'sql', 'extract', filename)
        
        pg_hook = PostgresHook(postgres_conn_id='source_db')
        with open(sql_file_path, 'r') as f:
            sql = f.read()
        
        sql = sql.replace(';', '\n WHERE updated_at >= NOW() - INTERVAL \'1 DAY\';')
            
        df = pg_hook.get_pandas_df(sql)
        logging.info(f"Extracted {len(df)} rows from source database")
        return df
    
    @task
    def upsert(filename: str, df: DataFrame):
        dags_folder = os.getenv('AIRFLOW__CORE__DAGS_FOLDER', '/opt/airflow/dags')
        sql_file_path = os.path.join(dags_folder, 'sql', 'insert', filename)
        
        pg_hook = PostgresHook(postgres_conn_id='warehouse_db')
        with open(sql_file_path, 'r') as f:
            sql = f.read()
        
        records =[ tuple(row) for row in df.itertuples(index=False, name=None)]

        for record in records:
            pg_hook.run(sql, parameters=record, autocommit=True)
    
    @task_group(group_id='dim_customer')
    def etlDimCustomer():
        df = extract('customers.sql')
        upsert('dim_customer.sql', df)
    
    @task_group(group_id='dim_product')
    def etlDimProduct():
        df = extract('products.sql')
        df = transform(df, ['stock_quantity'])
        upsert('dim_product.sql', df)
        
    etlDimCustomer() >> etlDimProduct()
    
    # Not supported yet as these tables does not have updated_at column
    # @task_group(group_id='dim_address')
    # def etlDimAddress():
    #     df = extract('addresses.sql')
    #     upsert('dim_address.sql', df)
    
    # @task_group(group_id='dim_category')
    # def etlDimCategory():
    #     df = extract('categories.sql')
    #     upsert('dim_category.sql', df)
    
    # @task_group(group_id='dim_customer_support')
    # def etlDimCustomerSupport():
    #     df = extract('customer_support.sql')
    #     upsert('dim_customer_support.sql', df)

    # etlDimCustomer() >> etlDimAddress() >> etlDimCategory() >> etlDimProduct() >> etlDimCustomerSupport()
    
daily_batch_etl()