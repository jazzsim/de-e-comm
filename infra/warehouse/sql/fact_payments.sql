DO $$
DECLARE dim_date_id INT;
BEGIN
    -- get todays date from dim_date table
    SELECT id INTO dim_date_id
    FROM dim_date
    WHERE full_date = CURRENT_DATE;

    -- insert into fact_payments
    INSERT INTO public.fact_payments
    (sale_id, payment_date_id, "payment_method", "payment_status", transaction_id)
    VALUES(:sale_id, dim_date_id, :payment_method, :payment_status, :transaction_id);
END $$