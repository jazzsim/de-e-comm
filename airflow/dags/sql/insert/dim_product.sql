INSERT INTO dim_product (id, "name", description, price, category_id, image_url, created_at, updated_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id)
DO UPDATE SET name = EXCLUDED.name, description = EXCLUDED.description, products = EXCLUDED.price, category_id = EXCLUDED.category_id, image_url = EXCLUDED.image_url, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;