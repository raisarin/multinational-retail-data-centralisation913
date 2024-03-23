-- Task 4: Sales from online
SELECT
	COUNT(orders_table.product_quantity) AS numbers_of_sales, 
	SUM(orders_table.product_quantity) AS product_quantity_count,
	CASE  
		WHEN dim_store_details.store_type = 'Web Portal' THEN 'Web' 
		ELSE 'Offline' 
	END AS location
FROM 
	orders_table
INNER JOIN 
	dim_store_details ON dim_store_details.store_code = orders_table.store_code
GROUP BY 
	location
ORDER BY 
	numbers_of_sales ASC;
