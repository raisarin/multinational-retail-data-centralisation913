-- In order_table make foreigen key to attach to the primary keys other tables
ALTER TABLE orders_table
	ADD CONSTRAINT order_card_key FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number),
	ADD CONSTRAINT order_date_key FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid),
	ADD CONSTRAINT order_products_key FOREIGN KEY (product_code) REFERENCES dim_products(product_code),
	ADD CONSTRAINT order_store_key FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code),
 	ADD CONSTRAINT order_user_key FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);

select * from orders_table;