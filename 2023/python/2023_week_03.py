# Preppin' Data 2023 Week 03

# Load packages
import pandas as pd
import numpy as np

# Input the data
target_df = pd.read_csv('2023//unprepped_data//PD 2023 Wk 3 Targets.csv')
transt_df = pd.read_csv('2023//unprepped_data//PD 2023 Wk 1 Input.csv')

# For the transactions file:
#  - Filter the transactions to just look at DSB 
#     - These will be transactions that contain DSB in the Transaction Code field
#  - Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values
#  - Change the date to be the quarter 
#  - Sum the transaction values for each quarter and for each Type of Transaction (Online or In-Person) 
transt_df['bank'] = transt_df['Transaction Code'].str.split('-',expand = True)[0]
transt_df = transt_df.loc[transt_df['bank'] == 'DSB']

transt_df['Online or In-Person'] = np.where(transt_df['Online or In-Person'] == 1,'Online','In-Person')

transt_df['Transaction Date'] = pd.to_datetime(transt_df['Transaction Date'], format='%d/%m/%Y %H:%M:%S')
transt_df['Quarter'] = transt_df['Transaction Date'].dt.quarter

transt_df = transt_df.groupby(['Online or In-Person','Quarter']).agg({'Value': 'sum'}).reset_index()

# For the targets file:
#  - Pivot the quarterly targets so we have a row for each Type of Transaction and each Quarter
#  - Rename the fields
#  - Remove the 'Q' from the quarter field and make the data type numeric 
target_df = pd.melt(target_df, id_vars=['Online or In-Person'], value_vars=['Q1','Q2','Q3','Q4'])
target_df.columns = ['Online or In-Person','Quarter','Quarterly Targets']
target_df['Quarter'] = target_df['Quarter'].str.replace('Q','')
target_df['Quarter'] = target_df['Quarter'].astype(int)

# Join the two datasets together 
#  - You may need more than one join clause!
df = transt_df.merge(target_df, on = ['Online or In-Person','Quarter'])

# Remove unnecessary fields
# Calculate the Variance to Target for each row
df['Variance to Targets'] = df['Value'] - df['Quarterly Targets']

# Output the data
df.to_csv('2023//python//outputs//pd2023wk03_output.csv',index = False)
