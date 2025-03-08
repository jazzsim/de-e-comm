DO $$
DECLARE v_customer_id INT;
BEGIN
    SELECT customer_id INTO v_customer_id
    FROM fact_sales
    WHERE id = :sale_id;

    UPDATE dim_cart
    SET sale_id = :sale_id
    WHERE customer_id = v_customer_id;

    -- Update fact_sales table
    UPDATE fact_sales
    SET order_status = 'Completed'
    WHERE id = :sale_id;

    -- Update fact_payments table
    UPDATE fact_payments
    SET payment_status = 'Paid'
    WHERE transaction_id = :transaction_id;
END $$