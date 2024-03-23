-- Task 6: Highest sales in each year with month
SELECT
	ROUND(
		CAST(SUM(dim_products.product_price * orders_table.product_quantity)
		AS NUMERIC), 2) 
	AS total_sales,
	dim_date_times.year AS year,
	dim_date_times.month AS month
FROM 
	orders_table
INNER JOIN
	dim_products ON dim_products.product_code = orders_table.product_code
INNER JOIN 
	dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid
GROUP BY 
	year, month 
ORDER BY 
	total_sales DESC
LIMIT
	10;
