-- Alter column data type in  dim_store_details table, 
ALTER TABLE dim_store_details
	ALTER COLUMN longitude TYPE FLOAT USING NULLIF(longitude, 'N/A')::DOUBLE PRECISION,
	ALTER COLUMN locality TYPE VARCHAR(255),
	ALTER COLUMN store_code TYPE VARCHAR(12), 
	ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
	ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
	ALTER COLUMN store_type TYPE VARCHAR(255),
	ALTER COLUMN latitude TYPE FLOAT USING latitude::DOUBLE PRECISION,
	ALTER COLUMN country_code TYPE VARCHAR(2),
	ALTER COLUMN continent TYPE VARCHAR(255);