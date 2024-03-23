-- Task 8: Sales of different store types in Germany
SELECT
	ROUND(
		CAST(SUM(dim_products.product_price * orders_table.product_quantity)
		AS NUMERIC), 2) 
	AS total_sales,
	dim_store_details.store_type AS store_type,
	dim_store_details.country_code AS country_code
FROM 
	orders_table
INNER JOIN
	dim_products ON dim_products.product_code = orders_table.product_code
INNER JOIN 
	dim_store_details ON dim_store_details.store_code = orders_table.store_code
WHERE 
	dim_store_details.country_code = 'DE'	
GROUP BY 
	store_type, country_code
ORDER BY 
	total_sales ASC;