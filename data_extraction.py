# %%
from sqlalchemy import text # fetch_data query
import pandas as pd
import tabula

class DataExtractor:
  def __init__(self, db_connector):
    self.db_connector = db_connector
  
  # def fetch_data(self, table_name): 
  #   try:
  #     with self.db_connector.engine.execution_options(isolation_level='AUTOCOMMIT').connect() as connection: 
  #       query = text(f"SELECT * FROM {table_name}")
  #       result = connection.execute(query)
  #       data = result.fetchall()
  #       return data
  #   except Exception as e: 
  #     print("Error: Fetching data failed\n", e)
    
  def read_rds_table(self, table_name): 
    try: 
      table_df = pd.read_sql_table(table_name, self.db_connector.engine)
      print(F"INFO: Dataframe read from table {table_name}")
      return table_df
    except Exception as e: 
      print("Error: Reading RDS table failed\n", e)
  
  # use "lattice=true" for more accurate table extraction and to avoid combining datas to single cell
  def retrieve_pdf_data(self, link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'):
    try: 
      pdf_list = tabula.read_pdf(link, stream=True, multiple_tables=False, pages='all', lattice=True)
      pdf_df = pdf_list[0]
      print("Info: PDF converted to Datafram from link")
      return pdf_df
    except Exception as e: 
      print("ERROR: Unable to retrieve PDF data\n", e)
     
# %%
