# %%
from sqlalchemy import text # fetch_data query
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
        table_df = pd.read_sql_table(table_name, self.db_connector.engine)
        print(F"INFO: Dataframe read from table {table_name}")
        return table_df
    except Exception as e: 
      print("Error: Reading RDS table failed\n", e)
# %%
