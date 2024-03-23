# %%creds_yaml
import yaml
from sqlalchemy import create_engine, inspect

class DatabaseConnector:
  def __init__(self, creds_file):
    self.creds_file = creds_file
    self.creds_data = self.read_db_creds()
    self.engine = self.init_db_engine()
    self.table_name = self.list_db_tables()

  def read_db_creds(self):
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
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    HOST = self.creds_data['RDS_HOST']
    USER = self.creds_data['RDS_USER']
    PASSWORD = self.creds_data['RDS_PASSWORD']
    DATABASE = self.creds_data['RDS_DATABASE']
    PORT = self.creds_data['RDS_PORT']
    try: 
      engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
      print(f"INFO: Database engine initilised with {self.creds_file}")
      return engine
    except Exception as e: 
      print("ERROR: Database engine initilisation failed\n", e)
    
  def list_db_tables(self): 
    try: 
      inspector = inspect(self.engine)
      table_name = inspector.get_table_names()
      print(f"Table in {self.creds_file} database:", table_name)
      return table_name
    except Exception as e: 
      print("Error: Table inspection failed\n", e)
  
  def upload_to_db(self, table_df, table_name):
    try: 
      table_df.to_sql(table_name, con=self.engine, if_exists='replace')  
      print(f"INFO: {table_name} has been uploaded to database")
    except Exception as e: 
      print("ERROR: Failed uploading table to database\n", e)
# %%
