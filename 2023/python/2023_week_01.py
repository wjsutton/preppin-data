# Preppin' Data 2023 Week 01

# load packages
import pandas as pd
import numpy as np

# Input the data
df = pd.read_csv('2023\\unprepped_data\\PD 2023 Wk 1 Input.csv')

# Split the Transaction Code to extract the letters at the start of the transaction code. 
# These identify the bank who processes the transaction
# Rename the new field with the Bank code 'Bank'. 
df['Bank'] = df['Transaction Code'].str.split('-',expand=True)[0]

# Rename the values in the Online or In-person field, 
# Online of the 1 values and In-Person for the 2 values. 
df['Online or In-Person'] = np.where(df['Online or In-Person'] == 1,'Online','In-Person')

# Change the date to be the day of the week 
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], format='%d/%m/%Y %H:%M:%S')
df['Transaction Date'] = df['Transaction Date'].dt.day_name()

# Different levels of detail are required in the outputs. 
# You will need to sum up the values of the transactions in three ways:
# 1. Total Values of Transactions by each bank
output_1 = df.groupby('Bank',as_index=False)['Value'].sum()

# 2. Total Values by Bank, Day of the Week and Type of Transaction (Online or In-Person)
output_2 = df.groupby(['Bank','Online or In-Person','Transaction Date'],as_index=False)['Value'].sum()

# 3. Total Values by Bank and Customer Code
output_3 = df.groupby(['Bank','Customer Code'],as_index=False)['Value'].sum()

# Output each data file
output_1.to_csv('2023\\python\\outputs\\pd2023wk01_output1.csv',index=False)
output_2.to_csv('2023\\python\\outputs\\pd2023wk01_output2.csv',index=False)
output_3.to_csv('2023\\python\\outputs\\pd2023wk01_output3.csv',index=False)

print('data prepped!')
