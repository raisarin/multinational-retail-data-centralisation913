import pandas as pd
from dateutil.parser import parse

class DataCleaning: 
  """
  DataCleaning class is called for cleaning the dataframe with appropriate functions.
  """

  def _clean_country_code(self, df):
    """
    Clean the country code column in the dataframe by replacing certain country code and limiting it to two characters.

    Parameters: 
      df (pd.dataframe): User dataframe to be cleaned. 

    Returns: 
      pd.dataframe: User dataframe with cleaned country code column.
    """
    df.loc[:,'country_code'] = df['country_code'].replace('GGB','GB')
    df = df[df['country_code'].str.len() == 2]
    return df
  
  def _clean_date(self, df, column_name):
    """
    Clean the date column from date dataframe with date formatting. 

    Parameters: 
      df (pd.dataframe): User dataframe to be cleaned.

    Returns: 
      pd.dataframe: User dataframe with cleaned date column.
    """
    df.loc[:,column_name] = df[column_name].apply(parse)
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    df.dropna(axis=0, subset=[column_name] ,inplace=True)
    df[column_name] = df[column_name].dt.strftime('%Y-%m-%d')
    return df
  
  def _clean_phone_number(self, df):
    """
    Clean the phone number column in the dataframe with certain phone number format. 

    Parameters: 
      df (pd.dataframe): User dataframe to be cleaned.

    Returns: 
      pd.dataframe: User dataframe with cleaned phone number column.
    """
    df['phone_number'] = df['phone_number'].replace({r'\+49':'0', r'\+44':'0', r'\(0\)':''}, regex=True)
    df['phone_number'] = df['phone_number'].replace({r'\D': ''}, regex=True)
    return df
    
  def clean_user_data(self, df):
    """
    Clean the user dataframe using different cleaning functions. 

    Parameters: 
      df (pd.dataframe): User dataframe to be cleaned.

    Returns: 
      pd.dataframe: Cleaned user dataframe. 
    """
    df = df.drop_duplicates()
    df = df[~df.isin(['NULL']).any(axis=1)]
    df = self._clean_country_code(df)
    df = self._clean_date(df, 'date_of_birth')
    df = self._clean_date(df, 'join_date')
    df = self._clean_phone_number(df)
    df = df.drop('index', axis=1)
    df.set_index('first_name', inplace=True)
    return df
  
  def _clean_card_number(self, df): 
    """
    Clean card number column from card dataframe by extracting the numbers only. 

    Parameters: 
      df (pd.dataframe): Card dataframe to be cleaned. 

    Returns: 
      pd.dataframe: Card dataframe with clean card number column. 

    Notes: 
    """
    df['card_number'] = df['card_number'].str.extract('(\\d+)')
    return df 
  
  def _clean_expiry_date(self, df): 
    """
    Clean expiry date column from card dataframe with month-day format.

    Parameters
      df (pd.dataframe): Card dataframe to be cleaned. 
    
    Returns: 
      pd.dataframe: Card dataframe with clean expiry date column. 
    """
    df['expiry_date'] = pd.to_datetime(df['expiry_date'], format='%m/%d', errors='coerce', exact=True)
    df.dropna(axis=0, inplace=True)
    df['expiry_date'] = df['expiry_date'].dt.strftime('%m/%d') 
    return df
  
  def _clean_card_provider(self, df):
    """
    Clean card provider column from card dataframe by filtering from a list.

    Parameters
      df (pd.dataframe): Card dataframe to be cleaned. 
    
    Returns: 
      pd.dataframe: Card dataframe with clean card provider column. 
    """
    card_provider_list = ['Diners Club / Carte Blanche', 'American Express', 
                          'JCB 16 digit', 'JCB 15 digit', 
                          'Maestro', 'Mastercard', 
                          'Discover', 'VISA 19 digit', 
                          'VISA 16 digit', 'VISA 13 digit']
    df = df[df['card_provider'].isin(card_provider_list)]
    df['card_provider'] = df['card_provider'].astype('string')
    return df
  
  def _clean_date_payment(self,df):
    """
    Clean date payment column from card dataframe with year-month-day format.

    Parameters
      df (pd.dataframe): Card dataframe to be cleaned. 
    
    Returns: 
      pd.dataframe: Card dataframe with clean date payment column. 
    """
    df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'], format='%Y-%m-%d', errors='coerce', exact=True)
    df.dropna(axis=0, inplace=True)
    return df

  def clean_card_data(self, df):
    """
    Clean card dataframe using various functions. 

    Parameters
      df (pd.dataframe): Card dataframe to be cleaned. 
    
    Returns: 
      pd.dataframe: Cleaned card dataframe. 
    """
    df = self._clean_card_number(df)
    df = self._clean_expiry_date(df)
    df = self._clean_card_provider(df)
    df = self._clean_date_payment(df)
    df.set_index('card_number', inplace=True)
    return df

  def clean_store_data(self, df): 
    """
    Clean different column in the store dataframe by limiting country code column to 2 characters, 
    renaming values in continent column, dropping unused column and cleaning opening date column. 

    Parameters
      df (pd.dataframe): Store dataframe to be cleaned. 
    
    Returns: 
      pd.dataframe: Cleaned store dataframe. 
    """
    df = df[df['country_code'].str.len() == 2]
    df.loc[:,'continent'] = df['continent'].replace({'eeEurope':'Europe', 'eeAmerica':'America'})
    df = df.drop(['lat', 'address'], axis=1)
    df = self._clean_date(df, 'opening_date')
    df['staff_numbers'] = df['staff_numbers'].str.extract('(\\d+)')
    df.set_index('longitude', inplace=True)
    df = df.drop_duplicates()
    return df

  def _eval_weight(self, weight): 
    """
    Perform evluation function on the weight input.  

    Parameters
      weight (str): Value in the weight column of product dataframe. 
    
    Returns: 
      int: If evluation function can be performed. 
      str: If evluation cannot be performed.
    """
    try: 
      return eval(str(weight))
    except: 
      return weight
    
  def _convert_product_weights(self, df): 
    """ 
    Convert the weight column of the product dataframe using the convertion dictionary. 

    Paramters: 
      df (pd.dataframe): Product dataframe to be cleaned. 

    Returns: 
      pd.dataframe: Product dataframe with cleaned weight column. 
    """
    convertion_table = { 
      'x':'*',
      'kg':'',
      'g':'/1000',
      'ml':'/1000',
      'oz':'/35.274',
      ' .':''
    }
    df.loc[:,'weight'] = df['weight'].replace(convertion_table, regex=True)
    df['weight'] = df['weight'].apply(self._eval_weight)
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
    df.dropna(axis=0, inplace=True)
    return df 
  
  def _clean_category(self, df): 
    """ 
    Clean category column of the product dataframe using the category list. 

    Paramters: 
      df (pd.dataframe): Product dataframe to be cleaned. 

    Returns: 
      pd.dataframe: Product dataframe with cleaned category column. 
    """  
    category = ['toys-and-games', 'sports-and-leisure', 'pets', 'homeware',
       'health-and-beauty', 'food-and-drink', 'diy']
    df = df[df['category'].isin(category)]
    df['category'] = df['category'].astype('string')
    return df
  
  def _clean_removed(self, df): 
    """ 
    Clean removed column of the product dataframe using the removed list. 

    Paramters: 
      df (pd.dataframe): Product dataframe to be cleaned. 

    Returns: 
      pd.dataframe: Product dataframe with cleaned removed column. 
    """      
    removed = ['Still_avaliable', 'Removed']
    df = df[df['removed'].isin(removed)]
    df['removed'] = df['removed'].astype('string')
    return df

  def clean_products_data(self, df): 
    """ 
    Clean product dataframe with different fucntions. 

    Paramters: 
      df (pd.dataframe): Product dataframe to be cleaned. 

    Returns: 
      pd.dataframe: Clean product dataframe. 
    """   
    df = self._convert_product_weights(df)
    df = self._clean_date(df, 'date_added')
    df = self._clean_category(df)
    df = self._clean_removed(df)
    df = df.drop('Unnamed: 0', axis=1)
    df.set_index('product_name', inplace=True)
    return df 

  def clean_orders_data(self, df):
    """
    Clean orders datafame by removing unnecessary columns.

    Returns: 
      pd.dataframe: Clean orders dataframe.
    """
    df = df.drop(['level_0','first_name','last_name','1'], axis=1)
    df.set_index('date_uuid', inplace=True)
    return df

  def _clean_time_period(self, df): 
    """
    Clean time period column in date time dataframe by filtering values using time period list. 

    Parameters: 
      df (pd.dataframe): Date time dataframe to be cleaned. 
    
    Returns: 
      pd.dataframe: Date time dataframe with clean time period column.
    """
    time_period_list = ['Evening', 'Morning', 'Midday', 'Late_Hours']
    df = df[df['time_period'].isin(time_period_list)]
    return df

  def clean_date_time_data(self, df): 
    """
    Clean date time dataframe using a function. 

    Parameters: 
      df (pd.dataframe): Date time dataframe to be cleaned. 
    
    Returns: 
      pd.dataframe: Clean date time dataframe.
    """
    df = self._clean_time_period(df)
    df.set_index('timestamp', inplace=True)
    return df 
