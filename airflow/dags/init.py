import datetime

from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime(2025, 2, 17),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

@dag(default_args=default_args, tags=['Initialization'], schedule="@once")
def initialize_warehouse_db():
    SQLExecuteQueryOperator(
        task_id="initialize_warehouse_db",
        conn_id="warehouse_db",
        sql="sql/initialize_warehouse_db.sql",
    )

initialize_warehouse_db()