-- In orders_table, alter column data type
ALTER TABLE orders_table
  ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid,
  ALTER COLUMN user_uuid TYPE UUID USING date_uuid::uuid,
  ALTER COLUMN card_number TYPE VARCHAR(19),
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN product_code TYPE VARCHAR(11),
	ALTER COLUMN product_quantity TYPE SMALLINT;