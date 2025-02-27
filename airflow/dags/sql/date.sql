WITH RECURSIVE date_series AS (
    SELECT 
        DATE '2025-01-01' AS full_date  -- Start date
    UNION ALL
    SELECT 
        (full_date + INTERVAL '1 day')::DATE  -- Ensure it stays as DATE
    FROM 
        date_series
    WHERE 
        full_date < DATE '2030-12-31'  -- End date (2 years)
)
INSERT INTO dim_date (full_date, quarter, year, month, day, week_of_year, day_of_week)
SELECT 
    full_date,
    EXTRACT(QUARTER FROM full_date) AS quarter,
    EXTRACT(YEAR FROM full_date) AS year,
    EXTRACT(MONTH FROM full_date) AS month,
    EXTRACT(DAY FROM full_date) AS day,
    EXTRACT(WEEK FROM full_date) AS week_of_year,
    TO_CHAR(full_date, 'Day') AS day_of_week
FROM date_series;