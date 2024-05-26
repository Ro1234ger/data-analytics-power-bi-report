
        -- Drop the existing view if it exists
        DROP VIEW IF EXISTS store_type_sales;

        -- Create the view for store type sales and orders
        CREATE VIEW store_type_sales AS
        SELECT
            dim_store.store_type,
            SUM(orders.total_orders) AS total_sales,
            SUM(orders.total_orders) * 100.0 / SUM(SUM(orders.total_orders)) OVER () AS percentage_of_total_sales,
            COUNT(orders.store_code) AS total_orders
        FROM orders
        JOIN dim_store ON orders.store_code = dim_store.store_code
        GROUP BY dim_store.store_type;

-- Query the view to check results
SELECT * FROM store_type_sales;
    