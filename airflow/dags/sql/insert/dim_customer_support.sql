INSERT INTO dim_customer_support (ticket_id, customer_name, email, phone, "issue_category", issue_description, date_created, resolution_date, "resolution_status")
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) 
DO UPDATE SET ticket_id = EXCLUDED.ticket_id, customer_name = EXCLUDED.customer_name, email = EXCLUDED.email, phone = EXCLUDED.phone, issue_category = EXCLUDED.issue_category, issue_description = EXCLUDED.issue_description, date_created = EXCLUDED.date_created, resolution_date = EXCLUDED.resolution_date, resolution_status = EXCLUDED.resolution_status;
