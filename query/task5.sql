-- Task 5: Percentage of sales of each store type
SELECT
	dim_store_details.store_type AS store_type, 
	ROUND(
		CAST(SUM(orders_table.product_quantity * dim_products.product_price)
		AS NUMERIC), 2) 
	AS total_sales,
	ROUND(CAST(SUM(orders_table.product_quantity * dim_products.product_price) /
		(SELECT 
				SUM(orders_table.product_quantity * dim_products.product_price) AS total_sales
			FROM 
				orders_table
		INNER JOIN
			dim_products ON dim_products.product_code = orders_table.product_code) * 100 AS NUMERIC), 2) 
	AS "percentage(%)"
FROM 
    orders_table
INNER JOIN 
    dim_store_details ON dim_store_details.store_code = orders_table.store_code
INNER JOIN
    dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY 
    store_type
ORDER BY 
    "percentage(%)" DESC;
