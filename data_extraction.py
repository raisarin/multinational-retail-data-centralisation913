# %%
from sqlalchemy import text # fetch_data query
import pandas as pd
import tabula
import requests
import boto3 
from botocore.exceptions import NoCredentialsError, ClientError

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
  def retrieve_pdf_data(self, pdf_link):
    try: 
      pdf_list = tabula.read_pdf(pdf_link, stream=True, multiple_tables=False, pages='all', lattice=True)
      pdf_df = pdf_list[0]
      print("Info: PDF converted to Datafram from link")
      return pdf_df
    except Exception as e: 
      print("ERROR: Unable to retrieve PDF data\n", e)
  
  def list_number_of_stores(self, endpoint, headers):
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200: 
      data = response.json()
      return data['number_stores']
    else: 
      print('ERROR: Request failed for List number of stores')
      print(f"ERROR: Request failed with status code: {response.status_code}")
      print(f"ERROR: Response Text: {response.text}")      

  def retrieve_stores_data(self, endpoint, headers, number_of_stores):
    store_data_list = []
    #session = requests.Session()
    for store_number in range(number_of_stores): 
      #response = session.get(f'{endpoint}{store_number}', headers=headers)
      response = requests.get(f'{endpoint}{store_number}', headers=headers)
      if response.status_code == 200: 
        data = response.json()
        data = pd.json_normalize(data)
        store_data_list.append(data)
      else: 
        print('ERROR: Request failed for retrive stores data')
        print(f"ERROR: Request failed with status code: {response.status_code}")
        print(f"ERROR: Response Text: {response.text}")   
    store_data = pd.concat(store_data_list).set_index('index')
    return store_data   
  
  def extract_from_s3(self, link, local_path):
    try: 
      bucket, key = link.replace("s3://","").split("/")
      s3 = boto3.client('s3')
      s3.download_file(bucket, key, local_path)
      df = pd.read_csv(local_path)
      return df
    
    except NoCredentialsError:
      print("ERROR: AWS credentials not found. Please configure your credentials.")

    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            print(f"ERROR: {bucket} bucket does not exist.")
        else:
            print("ERROR: Failed extraction from s3\n", e)

  def extract_from_https(self, link):
    response = requests.get(link)
    if response.status_code == 200: 
      df = pd.read_json(link)
      return df
    else: 
      print(f'ERROR: Request failed when extracting from {link}')
      print(f"ERROR: Request failed with status code: {response.status_code}")
      print(f"ERROR: Response Text: {response.text}") 
# %%
