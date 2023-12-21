# %%
import database_utils
from sqlalchemy import inspect

class DataExtractor:

  @classmethod
  def list_db_table(cls): 
    engine = database_utils.DatabaseConnector.init_db_engine()
    print("Database engine initilised from DataExtractor")
    print(engine)
    inspector = inspect(engine)
    table_name = inspector.get_table_names()
    print("Table name: ", table_name)
    return table_name
  