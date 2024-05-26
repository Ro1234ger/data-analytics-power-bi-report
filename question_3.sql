
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
    