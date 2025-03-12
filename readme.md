# E-commerce Case Study
A project created to help myself understand data engineering. 

The **aim** of this project would be be familiar with data engineering concepts such as **ETL, data warehouse, data modelling**, etc.

<img src=diagrams/project_outline.png alt="high-level project overview">

## Streamlit
Live metrics from warehouse database *(update every 10s)*

<img src=diagrams/streamlit.png alt="Streamlit Today's Sale Dashboard">


## Folder Structure

The project is separated into airflow folder and infra folder, each contains a docker compose file. Kindly refer to the `readme.md` in respective folders for further documentations.

```
Simplified overview of folder structure

.
├── airflow/
│   ├── dags/
│   │   ├── sql/
│   │   ├── daily_batch_etl.py
│   │   └── init.py
│   ├── docker-compose.yaml
│   └── requirements.txt
└── infra/
    ├── source/
    │   └── main.py
    ├── warehouse/
    │   └── main.py
    ├── docker-compose.yaml
    └── requirements.txt
```

## System Design
<img src=diagrams/system_design/dockers.png alt="Docker services">
<img src=diagrams/system_design/system_design.png alt="system design overview">


## Execute Project
Running this project isn't straightforward. We will have to make sure `warehouse_db` are synced with `source_db` before we start the scheduler. We would run `infra/source/main.py` to create database and generate fake data (customers, projects, categories, etc.), and run **Airflow** to initialize `warehouse_db` and sync both databases.

### Steps
1. `cd infra && docker compose up --build --watch`
2. Open a new terminal and run `cd airflow && docker compose up --build -d`
3. Login to **Airflow** on `localhost:8080` with `airflow` as credentials
4. Setup database connection on **Airflow**

    <img src=diagrams/execute_project/airflow_connections.png alt="Airflow connection UI">
    <img src=diagrams/execute_project/source_connection_string.png alt="source_db conenction string">
    <img src=diagrams/execute_project/warehouse_connection_string.png alt="warehouse_db conenction string">

5. Run `initialize_warehouse_db` DAG and wait for it to complete.
<img src=diagrams/airflow/dag_graph.png alt="success dag">

6. Open `./infra/source/main.py` and change `start_schedule` to `True`
7. Wait for `ecommerce-data-source` container to restart
8. Check `kafka-listener` container to verify the setup is completed
<img src=diagrams/execute_project/kafka_listener_log.png alt="success dag">

