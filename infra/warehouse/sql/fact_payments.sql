INSERT INTO public.fact_payments
(id, order_id, payment_date_id, "payment_method", "payment_status", transaction_id)
VALUES(%s, %s, %s, %s, %s, %s);