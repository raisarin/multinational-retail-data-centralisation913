-- Alter column data type in dim_users
ALTER TABLE dim_users
	ALTER COLUMN first_name TYPE VARCHAR(255),
	ALTER COLUMN last_name TYPE VARCHAR(255),
	ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE,
	ALTER COLUMN country_code TYPE VARCHAR(2),
	ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
	ALTER COLUMN join_date TYPE DATE USING join_date::DATE;