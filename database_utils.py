# %%
import yaml
from sqlalchemy import create_engine, inspect

class DatabaseConnector:
  creds_yaml = 'db_creds.yaml'

  @classmethod
  def read_db_creds(cls):
    try: 
      with open(cls.creds_yaml, 'r') as file:
        creds_data = yaml.safe_load(file) # Dealing with untrusted input file
      return creds_data
    except FileNotFoundError: 
      print("ERROR: File not found", e)
    except Exception as e: 
      print("ERROR: Unexpected error", e)

  @classmethod
  def init_db_engine(cls):
    creds_data = cls.read_db_creds()
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    HOST = creds_data['RDS_HOST']
    USER = creds_data['RDS_USER']
    PASSWORD = creds_data['RDS_PASSWORD']
    DATABASE = creds_data['RDS_DATABASE']
    PORT = creds_data['RDS_PORT']
    try: 
      engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
      engine.execution_options(isolation_level='AUTOCOMMIT').connect()
      print("Database engine initilised in DatabaseConnector")
      return engine
    except Exception as e: 
      print("ERROR: Database engine initilisation failed", e)
    
  @classmethod
  def list_db_table(cls): 
    engine = cls.init_db_engine()
    inspector = inspect(engine)
    table_name = inspector.get_table_names()
    print("Table in database: ", table_name)
    return table_name
# %%
