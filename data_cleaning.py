import pandas as pd
from dateutil.parser import parse

class DataCleaning: 

  ## for clean user data 
  def clean_country_code(self, df):
    df.loc[:,'country_code'] = df['country_code'].replace('GGB','GB')
    df = df[df['country_code'].str.len() == 2]
    return df
  
  # phone number 
  def clean_date(self, df, column_name):
    df.loc[:,column_name] = df[column_name].apply(lambda x: parse(str(x)) if not isinstance(x, pd.Timestamp) else x)
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    df.dropna(axis=0, inplace=True)
    df[column_name] = df[column_name].dt.strftime('%Y-%m-%d')
    return df
  
  def clean_phone_number(self, df):
    df['phone_number'] = df['phone_number'].replace({r'\+49':'0', r'\+44':'0', r'\(0\)':''}, regex=True)
    df['phone_number'] = df['phone_number'].replace({r'\D': ''}, regex=True)
    return df
    
  def clean_user_data(self, df):
    df = df.drop_duplicates()
    df = df[~df.isin(['NULL']).any(axis=1)]
    df = self.clean_country_code(df)
    df = self.clean_date(df, 'date_of_birth')
    df = self.clean_date(df, 'join_date')
    df = self.clean_phone_number(df)
    return df
  
  ## For cleaning card data
  def clean_card_number(self, df): 
    # 15587 = 55 + 56*277 + 20 <- (19 data + 1 heading)
    ## card_number errors

    # Card Number range between 16 - 19 digits
    # int64   9,223,372,036,854,775,807
    # uint64 18,446,744,073,709,551,615
    # int64 does not cover all 19 digit variations 

    df['card_number'] = pd.to_numeric(df['card_number'], errors='coerce', downcast='unsigned')
    df.dropna(axis=0, inplace=True)
    try: 
      # the type has been set to object as SQL does not support the use of uint64
      df['card_number'] = df['card_number'].astype('object')
    except Exception as e: 
      print("ERROR: Failed to clean card number column as unsigned integer\n", e)
    return df 
  
  def clean_expiry_date(self, df): 
    df['expiry_date'] = pd.to_datetime(df['expiry_date'], format='%m/%d', errors='coerce', exact=True)
    df.dropna(axis=0, inplace=True)
    df['expiry_date'] = df['expiry_date'].dt.strftime('%m/%d') 
    return df
  
  def clean_card_provider(self, df):
    card_provider_list = ['Diners Club / Carte Blanche', 'American Express', 
                          'JCB 16 digit', 'JCB 15 digit', 
                          'Maestro', 'Mastercard', 
                          'Discover', 'VISA 19 digit', 
                          'VISA 16 digit', 'VISA 13 digit']
    df = df[df['card_provider'].isin(card_provider_list)]
    df['card_provider'] = df['card_provider'].astype('string')
    return df
  
  def clean_date_payment(self,df):
    df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'], format='%Y-%m-%d', errors='coerce', exact=True)
    df.dropna(axis=0, inplace=True)
    return df

  def clean_card_data(self, df):
    df = self.clean_card_number(df)
    df = self.clean_expiry_date(df)
    df = self.clean_card_provider(df)
    df = self.clean_date_payment(df)
    return df

  def clean_store_data(self, df): 
    df = df[df['country_code'].str.len() == 2]
    df.loc[:,'continent'] = df['continent'].replace({'eeEurope':'Europe', 'eeAmerica':'America'})
    df = df.drop('lat', axis=1)
    df = self.clean_date(df, 'opening_date')
    df = df.drop_duplicates()
    return df
  
  def convert_product_weights(self, df): 
    df.dropna(axis=0, inplace=True)
    df = self.clean_date(df, 'date_added')
    convertion_table = { 
      'kg':'',
      'g':'/1000',
      'ml':'/1000',
      'oz':'/35.274',
      'x':'*',
      ' .':''
    }
    df.loc[:,'weight'] = df['weight'].replace(convertion_table, regex=True)
    df.dropna(axis=0, inplace=True)
    test = pd.to_numeric(df['weight'], errors='coerce')