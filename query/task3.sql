-- Task 3: Months with largest amount of sales
SELECT
	ROUND(
		CAST(SUM(orders_table.product_quantity * dim_products.product_price) 
		AS NUMERIC), 2) 
	AS total_sales,
	dim_date_times.month
FROM 
	orders_table
INNER JOIN 
	dim_products ON dim_products.product_code = orders_table.product_code
INNER JOIN 
	dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid
GROUP BY 
	dim_date_times.month
ORDER BY 
	total_sales DESC
LIMIT 
	6;