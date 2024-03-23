-- Alter the data type of column in dim_card_details table
ALTER TABLE dim_card_details
	ALTER COLUMN card_number TYPE VARCHAR(19),
	ALTER COLUMN expiry_date TYPE VARCHAR(5),
	ALTER COLUMN date_payment_confirmed TYPE DATE;