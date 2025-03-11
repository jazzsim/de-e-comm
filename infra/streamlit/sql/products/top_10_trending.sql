-- today's top 10 trending

SELECT name as "Name", ranked_products."Interest Score"
FROM dim_product dp
LEFT JOIN (
    SELECT product_id, SUM(quantity) AS "Interest Score", RANK() OVER (ORDER BY SUM(quantity) DESC) as rank
    FROM fact_cart_activity
    WHERE date_added = (SELECT id FROM dim_date WHERE full_date = %s)
    GROUP BY product_id
) ranked_products ON dp.id = ranked_products.product_id
WHERE ranked_products.rank <= 10
ORDER BY ranked_products."Interest Score" DESC