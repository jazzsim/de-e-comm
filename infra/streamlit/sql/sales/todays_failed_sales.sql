SELECT COUNT(*) AS total_orders
FROM public.fact_sales
WHERE order_date_id = (SELECT id FROM public.dim_date WHERE full_date = %s AND (order_status = 'Canceled'  OR order_status = 'Pending'));