# Apache Airflow
An Apache Airflow instance running on docker compose. There are only two dags, `initialize_warehouse_db` and `daily_batch_etl`. 

# initialize_warehouse_db
I decided to move the initialization of `warehouse_db` to Airflow after finishing the `daily_batch_etl` DAG. It can reuse the same SQL from the ETL process to initialize the tables with data from `source_db`.

<img src=../diagrams/airflow/dag_graph.png alt="initialize_warehouse_db dag graph">
<img src=../diagrams/airflow/task_group.png alt="task group">

# daily_batch_etl
A simple DAG to ETL the latest records based on `updated_at` column.

<img src=../diagrams/airflow/dag_graph2.png alt="initialize_warehouse_db dag graph">