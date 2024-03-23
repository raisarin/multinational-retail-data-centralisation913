#%%
from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning
aws_db_connector = DatabaseConnector("db_creds.yaml")
aws_db_extractor = DataExtractor(aws_db_connector)
local_db_connector = DatabaseConnector("sales_data_creds.yaml")

# %%
