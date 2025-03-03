INSERT INTO public.fact_order_details
(id, sale_id, product_id, quantity, unit_price, total_price)
VALUES(%s, %s, %s, %s, %s, %s);