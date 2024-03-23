# %%creds_yaml
import yaml
from sqlalchemy import create_engine, inspect

class DatabaseConnector:
  """ 
  DatabaseConnector class reads credentials from a yaml file to initilise a connection to a database in order to read or upload data.  
  
  Parameters: 
    creds_file (str): Path to yaml file with database credentials 

  Attributes: 
    creds_file (str): Path to yaml file with database credentials.
    creds_data (dict): Dictionary of the database credentials. 
    engine (sqlalchemy.engine.Engine): SQLAlchemy engine.
    table_name (list): List of table names in the database. 

  """

  def __init__(self, creds_file):
    """ 
    Initialise DatabaseConnector class instance.   

    Parameters: 
      creds_file (str): Path to the credentials.
    """
    self.creds_file = creds_file
    self.creds_data = self.read_db_creds()
    self.engine = self.init_db_engine()
    self.table_name = self.list_db_tables()

  def read_db_creds(self):
    """ 
    Read the credentials in a yaml file. 

    Returns: 
      dict: Dictionary of the database credentials. 

    Raises: 
      FileNotFoundError: If specified file is not found.
      Exception: If an unexpected error occurs.
    """
    try: 
      with open(self.creds_file, 'r') as file:
        creds_data = yaml.safe_load(file) # Dealing with untrusted input file
        print(f"INFO: Credentials Read from {self.creds_file}")
      return creds_data
    except FileNotFoundError as e: 
      print("ERROR: File not found\n", e)
    except Exception as e: 
      print("ERROR: Unexpected error\n", e)

  def init_db_engine(self):
    """
    Initialise an engine to connect to the server with the database using the database credentials 

    Returns: 
      sqlalchemy.engine.Engine: SQLAlchemy engine.

    Raises: 
      Exception: If initialisation of the database engine fails
    """
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    HOST = self.creds_data['RDS_HOST']
    USER = self.creds_data['RDS_USER']
    PASSWORD = self.creds_data['RDS_PASSWORD']
    DATABASE = self.creds_data['RDS_DATABASE']
    PORT = self.creds_data['RDS_PORT']
    try: 
      engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
      print(f"INFO: Database engine initialised with {self.creds_file}")
      return engine
    except Exception as e: 
      print("ERROR: Database engine initialisation failed\n", e)
    
  def list_db_tables(self): 
    """
    Show list of tables names that are stored in the database. 

    Returns: 
      list: Lists of table names.

    Raises: 
      Exception: If table inspection fails.
    """
    try: 
      inspector = inspect(self.engine)
      table_name = inspector.get_table_names()
      print(f"Table in {self.creds_file} database:", table_name)
      return table_name
    except Exception as e: 
      print("Error: Table inspection failed\n", e)
  
  def upload_to_db(self, clean_df, table_name):
    """
    Upload a clean dataframe with table name into the database server. 

    Parameters: 
      clean_df (pd.Dataframe): Cleaned dataframe to be upload to the database.
      table_name (str): Name of the table for the dataframe to be stored.

    Raises: 
      Exception: If uploading the dataframe fails.
    """
    try: 
      clean_df.to_sql(table_name, con=self.engine, if_exists='replace')  
      print(f"INFO: {table_name} has been uploaded to database")
    except Exception as e: 
      print("ERROR: Failed uploading dataframe to database\n", e)
# %%