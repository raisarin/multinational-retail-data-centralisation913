#%%
from utility.data_extraction import DataExtractor
from utility.database_utils import DatabaseConnector
from utility.data_cleaning import DataCleaning

if __name__ == "__main__":

  aws_db_connector = DatabaseConnector('db_creds.yaml')
  aws_db_extractor = DataExtractor(aws_db_connector)
  local_db_connector = DatabaseConnector('sales_data_creds.yaml')

  # %%
  # Task 3: Extact, clean and upload user data
  user_data = aws_db_extractor.read_rds_table('legacy_users')
  user_data_clean = DataCleaning().clean_user_data(user_data)
  local_db_connector.upload_to_db(user_data_clean, 'dim_users')

  # %%
  # Task 4: Extact, clean and upload card data
  pdf_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'
  card_data = DataExtractor().retrieve_pdf_data(pdf_link)
  card_data_clean = DataCleaning().clean_card_data(card_data)
  local_db_connector.upload_to_db(card_data_clean, 'dim_card_details')

  # %%
  # Task 5: Extract and clean details of each store
  number_of_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
  headers = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
  number_of_stores = DataExtractor().list_number_of_stores(number_of_stores_endpoint, headers)

  stores_details_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'
  stores_data = DataExtractor().retrieve_stores_data(stores_details_endpoint, headers, number_of_stores)
  stores_data_clean = DataCleaning().clean_store_data(stores_data)
  local_db_connector.upload_to_db(stores_data_clean, 'dim_store_details')

  # %%
  # Task 6: Extract and clean product details 
  product_link = 's3://data-handling-public/products.csv'
  product_local_path = 'products.csv'
  product_data = DataExtractor().extract_from_s3(product_link, product_local_path)
  product_data_clean = DataCleaning().clean_products_data(product_data)
  local_db_connector.upload_to_db(product_data_clean, 'dim_products')

  # %%
  # Task 7: Retrieve and clean order table 
  orders_data = aws_db_extractor.read_rds_table('orders_table')
  orders_data_clean = DataCleaning().clean_orders_data(orders_data)
  local_db_connector.upload_to_db(orders_data_clean, 'orders_table')

  # %%
  # Task 8: Retrieve and clean date event data 
  date_time_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
  date_time_data = DataExtractor().extract_from_https(date_time_link)
  date_time_data_clean = DataCleaning().clean_date_time_data(date_time_data)
  local_db_connector.upload_to_db(date_time_data_clean, 'dim_date_times')
  # %%
