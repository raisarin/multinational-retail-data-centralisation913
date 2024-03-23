#%%
from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning

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
card_data = DataExtractor().retrieve_pdf_data()
card_data_clean= DataCleaning().clean_card_data(card_data)
local_db_connector.upload_to_db(card_data_clean, 'dim_card_details')
# %%

# Task 5: Extract and clean details of each store
number_of_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
header = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
stores_data = DataExtractor().list_number_of_stores(number_of_stores_endpoint, header)