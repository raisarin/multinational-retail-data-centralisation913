# %%


# %%
#import database_utils as dbu
from sqlalchemy import text
import pandas as pd

class DataExtractor:
  def __init__(self, db_connector):
    self.db_connector = db_connector
  
  def fetch_data(self, table_name): 
    try:
      with self.db_connector.engine.execution_options(isolation_level='AUTOCOMMIT').connect() as connection: 
        query = text(f"SELECT * FROM {table_name}")
        result = connection.execute(query)
        data = result.fetchall()
        return data
    except Exception as e: 
      print("Error: Fetching data failed\n", e)
    
  def read_rds_table(self, table_name): 
    try: 
      with self.db_connector.engine.execution_options(isolation_level='AUTOCOMMIT').connect() as connection: 
        rds_pd = pd.read_sql_table('table_name', self.db_connector.engine)
        rds_pd.head(10)
        return rds_pd
    except Exception as e: 
      print("Error: Reading RDS table failed\n", e)
# %%
  check what is causing the error for the table to not load
  test in the database_tulis directly 
  if it runs there 
  export to the data_extraction 
# %%
