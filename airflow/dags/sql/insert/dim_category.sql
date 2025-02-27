INSERT INTO dim_category (id, name, description)
VALUES (%s, %s, %s)
ON CONFLICT (id) 
DO UPDATE SET name = EXCLUDED.name, description = EXCLUDED.description;
