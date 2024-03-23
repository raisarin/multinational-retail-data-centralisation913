import pandas as pd

class DataCleaning: 
  
  def clean_user_data(self, rds_pd):
    return

  def clean_card_data(self, pdf_df):
    #15587 = 55 + 56*277 + 20 <- (19 data + 1 heading)
    
    # Card Number range between 16 - 19 digits
    # int64   9,223,372,036,854,775,807
    # uint64 18,446,744,073,709,551,615
    # int64 does not cover all 19 digit variations 

    ## card_number errors
    pdf_df["card_number"] = pd.to_numeric(pdf_df["card_number"], errors='coerce', downcast='unsigned')
    pdf_df.dropna(axis=0, inplace=True)
    try: 
      pdf_df["card_number"] = pdf_df["card_number"].astype('uint64')
    except Exception as e: 
      print("ERROR: Failed to clean card number coloumn as unsigned integer\n", e)
    
    #expiry_date   
    pdf_df["expiry_date"] = pd.to_datetime(pdf_df["expiry_date"], format='%m/%d', errors='coerce', exact=True)
    pdf_df.dropna(axis=0, inplace=True)
    pdf_df["expiry_date"] = pdf_df["expiry_date"].dt.strftime('%m/%d')

    #card_provider 
    #date_payment_confirmed

    return pdf_df_clean


