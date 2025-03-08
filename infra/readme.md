# Infra
The docker compose contains the following containers
* Transactional Database (PostgreSQL)
<img src=../diagrams/source_erd.png>
* Warehouse Database (PostgreSQL)
<img src=../diagrams/warehouse_erd.png>

* Apache Zookeeper (zookeeper)
* Apache Kafka (kafka)
* Python script (ecommerce-data-source)
* Python script (kafka-listener)

## Kafka
Kafka will stream customer's actions into fact tables and other relevant tables. This will be a real-time ETL to display store performance in real time, check on product restock status, etc.

| Events                                                    |   Usage                                                   |
| :-------------------------------------------------------- |   :-----------------------------------------------------: |
| CREATE_CART<br>(*dim_cart*)                               |   Cart Conversion Rate                                    |
| ADD_TO_CART<br>(*fact_cart_activity*)                     |   Customer's Preference                                   |
| SALES<br>(*fact_sales*)                                   |   Analysis on sales performance                           |
| MAKE_PAYMENT<br>(*fact_payments*)                         |   Payment completion rate                                 |
| SUCCESS_SALE<br>(*dim_cart,fact_sales,fact_payments*)     |   Analysis on sales performance & Customer's Preference   |
| ORDER_DETAILS<br>(*fact_order_details*)                   |   Customer's Preference & Product performance             |


## ecommerce-data-source
The python script in `main.py` will randomly generate data to mock a ecommerce transaction database

### Logic
The python script will do the following:
* Select X amount of customers
* Add item(s) into their cart
* Remove item(s) from some user's cart
* Checkout cart (create sale order, make payment, update sale status, etc.)

In each actions, it will produce event to Kafka with relevant data.


## kafka-listener
A kafka consumer in python. Listen and insert data into `warehouse_db`.
