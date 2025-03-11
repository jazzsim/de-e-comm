CREATE TABLE dim_customer (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE dim_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE dim_product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id INTEGER REFERENCES dim_category(id),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE dim_cart (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES dim_customer(id) NOT NULL,
    cart_id INTEGER UNIQUE NOT NULL,
    sale_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE dim_date (
    id SERIAL PRIMARY KEY,
    full_date DATE NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    week_of_year INTEGER NOT NULL,
    day_of_week VARCHAR(20) NOT NULL
);

CREATE TYPE issue_category AS ENUM ('Billing', 'Technical Support', 'Account Management', 'Product Inquiry', 'Shipping', 'Returns and Refunds');
CREATE TYPE resolution_status AS ENUM ('Resolved', 'Pending', 'Escalated');

CREATE TABLE dim_customer_support (
    ticket_id VARCHAR(100) PRIMARY KEY UNIQUE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    issue_category issue_category NOT NULL,
    issue_description VARCHAR(255) NOT NULL,
    date_created VARCHAR(20) DEFAULT CURRENT_DATE NOT NULL,
    resolution_date VARCHAR(20) DEFAULT CURRENT_DATE,
    resolution_status resolution_status NOT NULL
);

CREATE TYPE order_status AS ENUM ('Pending', 'Completed', 'Canceled');

CREATE TABLE fact_sales (
    id SERIAL PRIMARY KEY,
    total_amount DECIMAL(10,2) NOT NULL,
    order_status ORDER_STATUS NOT NULL,
    order_date_id INTEGER REFERENCES dim_date(id) NOT NULL,
    customer_id INTEGER REFERENCES dim_customer(id) NOT NULL,
    payment_id INTEGER
);

CREATE TYPE payment_method AS ENUM ('Credit Card', 'E-Wallet');
CREATE TYPE payment_status AS ENUM ('Paid', 'Pending', 'Failed');

CREATE TABLE fact_payments (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES fact_sales(id) NOT NULL,
    payment_date_id INTEGER REFERENCES dim_date(id) NOT NULL,
    payment_method payment_method NOT NULL,
    payment_status payment_status NOT NULL,
    transaction_id VARCHAR(100) UNIQUE
);


-- Add in constraint for circular dependency --
ALTER TABLE fact_sales ADD CONSTRAINT fact_sales_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES fact_payments (id);
ALTER TABLE dim_cart ADD CONSTRAINT dim_cart_sale_id_fkey FOREIGN KEY (sale_id) REFERENCES fact_sales (id);


CREATE TABLE fact_order_details (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES fact_sales(id) NOT NULL,
    product_id INTEGER REFERENCES dim_product(id) NOT NULL,
    quantity INTEGER NOT NULL,
    total_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE fact_cart_activity (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES dim_cart(cart_id) NOT NULL,
    product_id INTEGER REFERENCES dim_product(id) NOT NULL,
    quantity INTEGER NOT NULL,
    date_added INTEGER REFERENCES dim_date(id) NOT NULL
);