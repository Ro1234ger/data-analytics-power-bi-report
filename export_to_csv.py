import psycopg2
import pandas as pd

# Database connection details
conn = psycopg2.connect(
    host="powerbi-data-analytics-server.postgres.database.azure.com",
    port="5432",
    database="orders-db",
    user="maya",
    password="AiCore127!"
)

queries = {
    "question_1": """
        SELECT SUM(staff_numbers) AS total_staff
        FROM dim_store
        WHERE country_code = 'GB';
    """,
    "question_2": """
        SELECT TO_CHAR(TO_DATE(order_date, 'YYYY-MM-DD'), 'Month') AS month, 
            SUM(orders.product_quantity * dim_product.sale_price) AS total_revenue
        FROM orders
        JOIN dim_product ON orders.product_code = dim_product.product_code
        WHERE EXTRACT(YEAR FROM TO_DATE(order_date, 'YYYY-MM-DD')) = 2022
        GROUP BY TO_CHAR(TO_DATE(order_date, 'YYYY-MM-DD'), 'Month')
        ORDER BY total_revenue DESC
        LIMIT 1;
    """,
    "question_3": """
        SELECT dim_store.store_type, 
            SUM(orders.product_quantity * dim_product.sale_price) AS total_revenue
        FROM orders
        JOIN dim_store ON orders.store_code = dim_store.store_code
        JOIN dim_product ON orders.product_code = dim_product.product_code
        WHERE dim_store.country = 'Germany'
            AND EXTRACT(YEAR FROM TO_DATE(orders.order_date, 'YYYY-MM-DD')) = 2022
        GROUP BY dim_store.store_type
        ORDER BY total_revenue DESC
        LIMIT 1;
    """,
    "question_4": """
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
    """,
    "question_5": """
        SELECT dim_product.category, SUM((dim_product.sale_price - dim_product.cost_price) * orders.product_quantity) AS total_profit
        FROM orders
        JOIN dim_store ON orders.store_code = dim_store.store_code
        JOIN dim_product ON orders.product_code = dim_product.product_code
        WHERE dim_store.country_region = 'Wiltshire' AND dim_store.country_code = 'GB' AND EXTRACT(YEAR FROM TO_DATE(orders.order_date, 'YYYY-MM-DD')) = 2021
        GROUP BY dim_product.category
        ORDER BY total_profit DESC
        LIMIT 1;
    """
}

for question, query in queries.items():
    df = pd.read_sql(query, conn)
    df.to_csv(f'F:/PowerBI/{question}.csv', index=False)
    with open(f'F:/PowerBI/{question}.sql', 'w') as file:
        file.write(query)

# Close the connection
conn.close()