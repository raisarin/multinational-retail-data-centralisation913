-- Alter the type for columns in dim_date_times table
ALTER TABLE dim_date_times 
	ALTER COLUMN month TYPE VARCHAR(2),
	ALTER COLUMN year TYPE VARCHAR(4),
	ALTER COLUMN day TYPE VARCHAR(2), 
	ALTER COLUMN time_period TYPE VARCHAR(10),
	ALTER COLUMN date_uuid TYPE uuid USING date_uuid::UUID;
