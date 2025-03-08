DO $$
DECLARE dim_date_id INT;
BEGIN
    -- Get today's date ID from dim_date table
    SELECT id INTO dim_date_id
    FROM dim_date
    WHERE full_date = CURRENT_DATE;

    -- Insert into fact_sales table using the fetched dim_date_id
    INSERT INTO public.fact_sales
    (total_amount, "order_status", order_date_id, customer_id)
    VALUES(:total_amount, :order_status, dim_date_id, :customer_id);
END $$
