INSERT INTO dim_customer (id, first_name, last_name, email, phone, date_of_birth, created_at, updated_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) 
DO UPDATE SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name, email = EXCLUDED.email, phone = EXCLUDED.phone, date_of_birth = EXCLUDED.date_of_birth, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;
