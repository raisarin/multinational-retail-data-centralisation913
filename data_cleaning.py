import pandas as pd
from dateutil.parser import parse

class DataCleaning: 
  
  def clean_country_code(self, df):
    df.loc[:,'country_code'] = df['country_code'].str.replace('GGB', 'GB')
    df = df[df['country_code'].str.len() == 2]
    return df
  
  #phone number 
  def clean_date(self, df, coloumn_name):
    df.loc[:,coloumn_name] = df[coloumn_name].apply(parse)
    df[coloumn_name] = pd.to_datetime(df[coloumn_name], errors='coerce')
    df.dropna(axis=0, inplace=True)
    df[coloumn_name] = df[coloumn_name].dt.strftime('%Y-%m-%d')
    return df
  
  def clean_phone_number(self, df):
    df['phone_number'] = df['phone_number'].replace({r'\+49':'0', r'\+44':'0', r'\(0\)':''}, regex=True)
    df['phone_number'] = df['phone_number'].replace({r'\D': ''}, regex=True)
    return df
    
  def clean_user_data(self, df):
    df.drop_duplicates()
    df = df[~df.isin(['NULL']).any(axis=1)]
    df = self.clean_country_code(df)
    df = self.clean_date(df, 'date_of_birth')
    df = self.clean_date(df, 'join_date')
    df = self.clean_phone_number(df)
    return df
  
  move all the function in the different def functions 
  
  def clean_card_number(self, df): 

  def clean_card_data(self, df):
    #15587 = 55 + 56*277 + 20 <- (19 data + 1 heading)
    ## card_number errors

    # Card Number range between 16 - 19 digits
    # int64   9,223,372,036,854,775,807
    # uint64 18,446,744,073,709,551,615
    # int64 does not cover all 19 digit variations 

    df['card_number'] = pd.to_numeric(df['card_number'], errors='coerce', downcast='unsigned')
    df.dropna(axis=0, inplace=True)
    try: 
      df['card_number'] = df['card_number'].astype('uint64')
    except Exception as e: 
      print("ERROR: Failed to clean card number coloumn as unsigned integer\n", e)
    
    #expiry_date   
    df['expiry_date'] = pd.to_datetime(df['expiry_date'], format='%m/%d', errors='coerce', exact=True)
    df.dropna(axis=0, inplace=True)
    df['expiry_date'] = df['expiry_date'].dt.strftime('%m/%d')

    #card_provider 
    df['card_provider'] = df['card_provider'].astype('string')

    #date_payment_confirmed
    df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'], format='%Y-%m-%d', errors='coerce', exact=True)
    df.dropna(axis=0, inplace=True)
    return df


