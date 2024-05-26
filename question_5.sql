
        SELECT dim_product.category, SUM((dim_product.sale_price - dim_product.cost_price) * orders.product_quantity) AS total_profit
        FROM orders
        JOIN dim_store ON orders.store_code = dim_store.store_code
        JOIN dim_product ON orders.product_code = dim_product.product_code
        WHERE dim_store.country_region = 'Wiltshire' AND dim_store.country_code = 'GB' AND EXTRACT(YEAR FROM TO_DATE(orders.order_date, 'YYYY-MM-DD')) = 2021
        GROUP BY dim_product.category
        ORDER BY total_profit DESC
        LIMIT 1;
    