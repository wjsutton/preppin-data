# Preppin' Data 2023 Week 04

# Load packages
import pandas as pd
import numpy as np

# Input the data
# We want to stack the tables on top of one another, since they have the same fields in each sheet.
# Some of the fields aren't matching up as we'd expect, due to differences in spelling. Merge these fields together

# Read all Excel tabs and concat as one dateframe
all_tabs = pd.read_excel('2023//unprepped_data//PD 2023 Wk 4 New Customers.xlsx', engine='openpyxl' ,sheet_name=None)

# Bring all the sheets together
all_dfs = []
for tab_name, df in all_tabs.items():
    df.columns = ['ID' ,'Joining Day','Demographic','Value']
    df['sheet_name'] = tab_name
    all_dfs.append(df)
    combined_df = pd.concat(all_dfs, ignore_index=True)

# Make a Joining Date field based on the Joining Day, Table Names and the year 2023
combined_df['Joining Month'] = pd.to_datetime(combined_df['sheet_name'], format= '%B').dt.strftime("%m")
combined_df['Joining Date'] = '2023-' + combined_df['Joining Month'].astype(str) + '-' + combined_df['Joining Day'].astype(str)
combined_df['Joining Date'] = pd.to_datetime(combined_df['Joining Date'], format= '%Y-%m-%d')

# Now we want to reshape our data so we have a field for each demographic, for each new customer
combined_df = combined_df[['ID','Joining Date','Demographic','Value']]
pivot_df = pd.pivot(combined_df,index=['ID','Joining Date'],columns='Demographic',values='Value').reset_index()

# Make sure all the data types are correct for each field
pivot_df['Date of Birth'] = pd.to_datetime(pivot_df['Date of Birth'], format='%m/%d/%Y')

# Remove duplicates
# If a customer appears multiple times take their earliest joining date
pivot_df['rank'] = pivot_df.groupby(['ID'])['Joining Date'].rank(method="first", ascending=True)
pivot_df = pivot_df.loc[pivot_df['rank'] == 1]
del pivot_df['rank']

# Output the data
pivot_df.to_csv('2023//python//outputs//pd2023wk04_output.csv',index = False)