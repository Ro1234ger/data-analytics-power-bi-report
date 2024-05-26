
        SELECT TO_CHAR(TO_DATE(order_date, 'YYYY-MM-DD'), 'Month') AS month, 
            SUM(orders.product_quantity * dim_product.sale_price) AS total_revenue
        FROM orders
        JOIN dim_product ON orders.product_code = dim_product.product_code
        WHERE EXTRACT(YEAR FROM TO_DATE(order_date, 'YYYY-MM-DD')) = 2022
        GROUP BY TO_CHAR(TO_DATE(order_date, 'YYYY-MM-DD'), 'Month')
        ORDER BY total_revenue DESC
        LIMIT 1;
    