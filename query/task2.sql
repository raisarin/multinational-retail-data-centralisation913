-- Task 2: Location with most stores
SELECT 
	locality,
	COUNT(locality) AS total_no_stores
FROM 
	dim_store_details
GROUP BY 
	locality
ORDER BY 
	total_no_stores DESC
LIMIT 
	7;