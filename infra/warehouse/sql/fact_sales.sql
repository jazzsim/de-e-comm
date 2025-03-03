INSERT INTO public.fact_sales
(id, total_amount, "order_status", order_date_id, customer_id, shipping_address_id, billing_address_id, payment_id)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s);