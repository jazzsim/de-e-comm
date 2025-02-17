# E-commerce Case Study
A project created to help myself understand data engineering. 

The **aim** of this project would be be familiar with data engineering concepts such as **ETL, data warehouse, data modelling**, etc.

<img src=diagrams/project_outline.png alt="high-level project overview">

## Source Systems 
The project consists of two kind of source systems. 
- Operational database (PostgreSQL)
- FTP server

The operational database is a simple e-commerce
<img src=diagrams/source_erd.png>

**User activities and sales data will be randomly generated on a schedule.*

The FTP server mimic a scenerio where a customer support report is uploaded daily. The report consists of the new tickets and any previous tickets that got resolved on that day. After a new report is uploaded, the previous report will be deleted.

## Dashboard
The dashboard will present basic analysis about sales, products and customers. There will also be fake live metrics streaming from Kafka, namely website interactions and customer's actions related to store.

<!-- link to dashboard -->

## Data Warehouse
Based on the requirements of the Dashboard, I decided to design the data warehouse with Star schema. Mainly because the operational database schema is very simple. Which also leads to the data warehouse being very similar to the source.

### ERD
<img src=diagrams/warehouse_erd.png>

<!-- Data warehouse ERD -->

### ETL
For this project, most of the ETL are normal ingestion, with some minor adjustment such as intorducing `dim_date` field to some of the tables.

For the FTP server, we have the following conditions:<br>
*The csv will only contains that day's tickets*<br>
*Only older ticket that is resolved will be included the csv*<br>
*If ticket is not resolved after 7 days, it should be closed*

### Kafka
Kafka will stream customer's store and checkout actions into `fact_cart_activity` and `fact_product_stock`. This will be a real-time ETL to display store performance in real time and check on product restock status.