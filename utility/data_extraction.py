# %%
from sqlalchemy import text # fetch_data query
import pandas as pd
import tabula
import requests
import boto3 
from botocore.exceptions import NoCredentialsError, ClientError

class DataExtractor:
  """ 
  DataExtractor class uses the engine from the DatabaseConnector to extract data from the database.

  Parameters: 
    db_connector (DatabaseConnector object): DatabaseConnector object.
  
  Attributes: 
    db_connector (DatabaseConnector object): DatabaseConnector object.
  """

  def __init__(self, db_connector=None):
    """ 
    Initialise DataExtractor class instance. 

    Parameters: 
        db_connector (DatabaseConnector object): DatabaseConnector object.
    """
    self.db_connector = db_connector

  def read_rds_table(self, table_name): 
    """
    Use the database engine to connect and read the table and convert it to dataframe.

    Parameters: 
      table_name (str): Name of table to be read. 

    Returns: 
      pd.Dataframe: Dataframe of the table. 

    Raises: 
      Exception: If table cannot be read. 
    """
    try: 
      table_df = pd.read_sql_table(table_name, self.db_connector.engine)
      print(F"INFO: Dataframe read from table {table_name}")
      return table_df
    except Exception as e: 
      print("Error: Reading RDS table failed\n", e)
  
  def retrieve_pdf_data(self, pdf_link):
    """ 
    Read the data of the PDF from the link and convert to dataframe. 

    Parameters:
      pdf_link (str): URL of the PDF. 

    Returns: 
      pd.Dataframe: Dataframe of the data in the PDF. 

    Raises: 
      Exception: If PDF data retrieval fails. 

    Notes: 
      Use "lattice=true" for more accurate table extraction and to avoid combining datas to single cell. 
    """
    try: 
      pdf_list = tabula.read_pdf(pdf_link, stream=True, multiple_tables=False, pages='all', lattice=True)
      pdf_df = pdf_list[0]
      print("Info: PDF converted to Dataframe from link")
      return pdf_df
    except Exception as e: 
      print("ERROR: Unable to retrieve PDF data\n", e)
  
  def list_number_of_stores(self, endpoint, headers):
    """
    Connect to the database using endpoint and headers to find the number of stores. 

    Parameters: 
      endpoint (str): API endpoint of the store data. 
      headers (str): Request header.

    Returns: 
      int: Number of stores.

    Notes: 
      If reponses of the request is not OK, an error message will let the user know the type and message of the error response. 
    """
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200: 
      data = response.json()
      print("INFO: Number of stores extracted")
      return data['number_stores']
    else: 
      print("ERROR: Request failed for List number of stores")
      print(f"ERROR: Request failed with status code: {response.status_code}")
      print(f"ERROR: Response Text: {response.text}")      

  def retrieve_stores_data(self, endpoint, headers, number_of_stores):
    """ 
    Retrieve data from the store database using the endpoint, headers and store number. 

    Parameters: 
      endpoint (str): API endpoint of the store data. 
      headers (str): Request header. 
      number_of_stores (int): The number of stores in the database. 

    Returns: 
      pd.Dataframe: Dataframe of the data stored in each of the stores. 

    Notes: 
      If reponses of the request is not OK, an error message will let the user know the type and message of the error response.
      The request will take a while to load, there are comments suggestion tha can be enable to for faster reading of the data 
        but some of the data will not be read. 
    """
    store_data_list = []
    #session = requests.Session()
    for store_number in range(number_of_stores):
      response = requests.get(f'{endpoint}{store_number}', headers=headers)
      #response = session.get(f'{endpoint}{store_number}', headers=headers)
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
    """
    Extract the dataframe of csv file in the amazon bucket.

    Parameters: 
      link (str): URL of the location of the bucket.
      local_path (str): Location to export the dataframe.
    
    Returns: 
      pd.dataframe: Dataframe of the csv file. 

    Raises: 
      NoCredentialsError: If AWS credential are not found.
      ClientError: If bucket is not found otherwise shows error that extraction has failed.
    """
    try: 
      bucket, key = link.replace("s3://","").split("/")
      s3 = boto3.client('s3')
      s3.download_file(bucket, key, local_path)
      df = pd.read_csv(local_path)
      print("INFO: Data extracted from S3 bucket")
      return df
    
    except NoCredentialsError:
      print("ERROR: AWS credentials not found. Please configure your credentials.")

    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            print(f"ERROR: {bucket} bucket does not exist.")
        else:
            print("ERROR: Failed extraction from s3\n", e)

  def extract_from_https(self, link):
    """
    Extract dataframe from a HTTPS link containing json file.

    Parameters: 
      link (str): Link to the json file. 
    
    Returns: 
      pd.dataframe: Dataframe of the json file. 
    
    Notes: 
      If reponses of the request is not OK, an error message will let the user know the type and message of the error response.
    """
    response = requests.get(link)
    if response.status_code == 200: 
      df = pd.read_json(link)
      print("INFO: Data extracted from link")
      return df
    else: 
      print(f'ERROR: Request failed when extracting from {link}')
      print(f"ERROR: Request failed with status code: {response.status_code}")
      print(f"ERROR: Response Text: {response.text}") 
# %%
