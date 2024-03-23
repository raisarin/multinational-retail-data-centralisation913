-- Alter column data type in orders_table
ALTER TABLE orders_table
  ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
  ALTER COLUMN user_uuid TYPE UUID USING date_uuid::UUID,
  ALTER COLUMN card_number TYPE VARCHAR(19),
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN product_code TYPE VARCHAR(11),
	ALTER COLUMN product_quantity TYPE SMALLINT;