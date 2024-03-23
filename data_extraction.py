# %%
from sqlalchemy import text # fetch_data query
import pandas as pd
import tabula
import requests

class DataExtractor:
  def __init__(self, db_connector=None):
    self.db_connector = db_connector

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
  
  def list_number_of_stores(self, endpoint, header):
    response = requests.get(endpoint, headers=header)
    if response.status_code == 200: 
      data = response.json()
      return data['number_stores']
    else: 
      print(f"ERROR: Request failed with status code: {response.status_code}")
      print(f"ERROR: Response Text: {response.text}")      
  
  def retrieve_stores_data(self, endpoint):
# %%
