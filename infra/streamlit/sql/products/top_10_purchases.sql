-- today's top 10 products

SELECT name as "Name", ranked_products."Total Sold"
FROM dim_product dp
LEFT JOIN (
    SELECT product_id, SUM(quantity) AS "Total Sold", RANK() OVER (ORDER BY SUM(quantity) DESC) as rank
    FROM fact_order_details
    WHERE sale_id IN (
    SELECT id 
    FROM fact_sales
    WHERE order_status = 'Completed' AND order_date_id = (SELECT id FROM dim_date WHERE full_date = %s)
    )
    GROUP BY product_id
) ranked_products ON dp.id = ranked_products.product_id
WHERE ranked_products.rank <= 10
ORDER BY ranked_products."Total Sold" DESC