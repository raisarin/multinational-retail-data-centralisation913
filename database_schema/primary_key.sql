-- In order_table make forigen key to attach to the primary keys other 
ALTER TABLE dim_card_details 
	ADD PRIMARY KEY (card_number);
	
ALTER TABLE dim_date_times 
	ADD PRIMARY KEY (date_uuid);
	
ALTER TABLE dim_products 
	ADD PRIMARY KEY (product_code);
	
ALTER TABLE dim_store_details 
	ADD PRIMARY KEY (store_code);
	
ALTER TABLE dim_users 
	ADD PRIMARY KEY (user_uuid);
