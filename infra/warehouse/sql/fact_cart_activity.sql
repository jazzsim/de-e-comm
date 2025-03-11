DO $$
DECLARE dim_date_id INT;
BEGIN
    -- get todays date from dim_date table
    SELECT id INTO dim_date_id
    FROM dim_date
    WHERE full_date = CURRENT_DATE;

    INSERT INTO public.fact_cart_activity
    (cart_id, product_id, quantity, date_added)
    VALUES(:cart_id, :product_id, :quantity, dim_date_id);
END $$