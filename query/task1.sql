-- Task 1: Country and total number of stores
SELECT 
	country_code AS country,
	COUNT(country_code) AS total_no_stores
FROM 
	dim_store_details
GROUP BY 
	country_code
ORDER BY 
	total_no_stores DESC;