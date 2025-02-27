INSERT INTO dim_address (id, customer_id, street, city, state, postal_code, country, is_default_shipping, is_default_billing)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) 
DO UPDATE SET customer_id = EXCLUDED.customer_id, street = EXCLUDED.street, city = EXCLUDED.city, state = EXCLUDED.state, postal_code = EXCLUDED.postal_code, country = EXCLUDED.country, is_default_billing = EXCLUDED.is_default_billing, is_default_shipping = EXCLUDED.is_default_shipping;
