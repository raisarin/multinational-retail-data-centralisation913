-- Sales of company thoughtout the years
SELECT
	year, 
	CONCAT(
		'"hours": ', EXTRACT(HOUR FROM AVG(sale_time_diff)), ', ', 
		'"minutes": ', EXTRACT(MINUTE FROM AVG(sale_time_diff)), ', ', 
		'"seconds": ', EXTRACT(SECOND FROM AVG(sale_time_diff))::INT, ', ', 
		'"milliseconds": ', EXTRACT(MILLISECONDS FROM AVG(sale_time_diff))::INT
	) AS actual_time_taken
FROM(
	SELECT 
		year,
		sale_time,
		LEAD(sale_time) OVER(ORDER BY sale_time ASC) AS sale_time_next,
		LEAD(sale_time) OVER(ORDER BY sale_time ASC) - sale_time AS sale_time_diff
	FROM(
		SELECT 
			year,
			CAST(CONCAT(year, '-', month, '-', day, ' ', timestamp) AS TIMESTAMP) 
			AS sale_time
			FROM 
				dim_date_times
	)
)	
GROUP BY 
	year
ORDER BY
	AVG(sale_time_diff) DESC
LIMIT 5;