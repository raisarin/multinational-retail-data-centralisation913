# %%
import database_utils
from sqlalchemy import text

class DataExtractor:

  def __init__(self, db_connector):
    self.db_connector = db_connector
  
  def read_data(self, table_name): 
    try:
      with self.db_connector.execution_options(isolation_level='AUTOCOMMIT').connect() as connection: 
        query = text(f"SELECT * FROM {table_name}")
        result = connection.execute(query)
        data = result.fetchall()
        return data
    except Exception as e: 
      print("Error: Data extraction failed\n", e)
# %%
