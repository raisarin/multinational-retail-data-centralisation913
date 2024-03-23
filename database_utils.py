# %%
import yaml
from sqlalchemy import create_engine, inspect

class DatabaseConnector:
  def __init__(self, creds_yaml = 'db_creds.yaml'):
    self.creds_yaml = creds_yaml
    self.creds_data = self.read_db_creds()
    self.engine = self.init_db_engine()

  def read_db_creds(self):
    try: 
      with open(self.creds_yaml, 'r') as file:
        creds_data = yaml.safe_load(file) # Dealing with untrusted input file
        print("INFO: Credentials Read")
      return creds_data
    except FileNotFoundError: 
      print("ERROR: File not found\n", e)
    except Exception as e: 
      print("ERROR: Unexpected error\n", e)

  def init_db_engine(self):
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    HOST = self.creds_data['RDS_HOST']
    USER = self.creds_data['RDS_USER']
    PASSWORD = self.creds_data['RDS_PASSWORD']
    DATABASE = self.creds_data['RDS_DATABASE']
    PORT = self.creds_data['RDS_PORT']
    try: 
      engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
      print("INFO: Database engine initilised in DatabaseConnector")
      return engine
    except Exception as e: 
      print("ERROR: Database engine initilisation failed\n", e)
    
  def list_db_tables(self): 
    try: 
      inspector = inspect(self.engine)
      table_name = inspector.get_table_names()
      print("Table in database: ", table_name)
      return table_name
    except Exception as e: 
      print("Error: Engine inspection failed\n", e)

# %%
