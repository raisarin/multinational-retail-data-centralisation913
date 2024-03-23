-- Remove £ from product_price
UPDATE dim_products
	SET product_price = REPLACE(product_price, '£', '');

-- Add weight calss into dim_products table
ALTER TABLE dim_products
 	ADD COLUMN weight_class VARCHAR(14);
	
-- Set the weight class of the products
UPDATE dim_products
	SET weight_class = 
		CASE 
			WHEN weight < 2 THEN 'Light'
			WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
			WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
			ELSE 'Truck_required'
		END;
		
-- Rename column sill_available to dim_products
ALTER TABLE dim_products
	RENAME removed TO still_available;

-- Alter column type in dim_product table 
-- NOTE: There was as spelling mistake in database for "Still_avaliable"
ALTER TABLE dim_products
	ALTER COLUMN product_price TYPE FLOAT USING product_price::DOUBLE PRECISION,
	ALTER COLUMN weight TYPE FLOAT USING weight::DOUBLE PRECISION,
	ALTER COLUMN "EAN" TYPE VARCHAR(17),
	ALTER COLUMN product_code TYPE VARCHAR(11),
	ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
	ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
	ALTER COLUMN still_available TYPE BOOL USING 
		CASE WHEN still_available = 'Still_avaliable' THEN TRUE 
		ELSE FALSE
		END,
	ALTER COLUMN weight_class TYPE VARCHAR(14);