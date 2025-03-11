import streamlit as st
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import datetime
import time

DB_CONN = "postgresql://warehouse_user:warehouse_password@localhost:5434/warehouse_db"
# DB_CONN = "postgresql://warehouse_user:warehouse_password@warehouse-postgresql/warehouse_db"

def load_sql(file_path):
    with open(file_path, 'r') as file:
        query = file.read()
    return query

def execute_sql(query: str, params):
    try:
        engine = create_engine(DB_CONN)
        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to get today's sales
def get_todays_sales():
    today = datetime.date.today()
    query = load_sql('sql/sales/todays_sales.sql')
    return execute_sql(query, params=(today.strftime('%Y-%m-%d'),))

def get_todays_failed_sales():
    today = datetime.date.today()
    query = load_sql('sql/sales/todays_failed_sales.sql')
    return execute_sql(query, params=(today.strftime('%Y-%m-%d'),))

def get_top_10_products():
    today = datetime.date.today()
    query = load_sql('sql/products/top_10_purchases.sql')
    return execute_sql(query, params=(today.strftime('%Y-%m-%d'),))

def get_top_10_trending():
    today = datetime.date.today()
    query = load_sql('sql/products/top_10_trending.sql')
    return execute_sql(query, params=(today.strftime('%Y-%m-%d'),))

# Streamlit UI
st.title("Today's Sales Dashboard")

# Auto-refresh loop
while True:
    if st.button("Refresh", icon="🔄"):
        st.rerun()    
    
    # Sales
    sales = get_todays_sales() # success sales
    if sales is not None:
        col1, col2= st.columns(2)
        
        total_order = sales['total_orders'][0]
        total_sales = f"{sales['total_sales'][0]:,.2f}" if total_order > 0 else "0.00"
        
        col1.metric(label="Total Successful Orders", value=f"{total_order}", border=True)
        col2.metric(label="Total Sales", value=f"${total_sales}", border=True)
        
        failed_sales = get_todays_failed_sales()
        if failed_sales is not None:
            failed_order = failed_sales['total_orders'][0] if failed_sales['total_orders'][0] > 0 else 0
            if failed_order > 0:
                # in percent
                st.metric(label="Uncompleted Orders", value=f"{ failed_order / total_order * 100:,.2f} %", border=True, help=f"{failed_order} uncompleted orders out of {total_order} orders")
    
    # Products tabs
    tab1, tab2 =st.tabs(["Best Selling", "Trending"])
    
    with tab1:
        top_10_purchased = get_top_10_products()
        st.subheader("Most Purchased Products", help="Data from fact_order_details")
        if top_10_purchased is not None and len(top_10_purchased) != 0:
            st.dataframe(top_10_purchased, hide_index=True)
        else:
            st.info("No data available.")
    with tab2:
        top_10_interested = get_top_10_trending()
        st.subheader("Most Interested Products", help="Data from fact_cart_activty")
        if top_10_interested is not None and len(top_10_interested) != 0:
            st.dataframe(top_10_interested, hide_index=True)
        else:
            st.info("No data available.")
    
    time.sleep(10)  # Refresh every 10 seconds
    st.rerun()