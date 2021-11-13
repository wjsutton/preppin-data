# Preppin' Data 2021 Week 43
import pandas as pd
import numpy as np
import datetime

# Load data
unit_a_df = pd.read_excel('unprepped_data\\PD 2021 Wk 43 Input.xlsx', sheet_name='Business Unit A ')
unit_b_df = pd.read_excel('unprepped_data\\PD 2021 Wk 43 Input.xlsx', sheet_name='Business Unit B ',skiprows=5)
risk_df = pd.read_excel('unprepped_data\\PD 2021 Wk 43 Input.xlsx', sheet_name='Risk Level')

# From the Business Unit A Input, create a Date Lodged field
# remove NaNs and convert columns types
unit_a_df = unit_a_df[unit_a_df['Ticket ID'].notnull()]
unit_a_df['Rating'] = unit_a_df['Rating'].astype(int)
unit_a_df['Ticket ID'] = unit_a_df['Ticket ID'].astype(int)
unit_a_df['Year'] = unit_a_df['Year'].astype(int)
unit_a_df['Month'] = unit_a_df['Month '].astype(int)
unit_a_df['Day'] = unit_a_df['Date'].astype(int)

# create date parts to date
unit_a_df['dateInt']=unit_a_df['Year'].astype(str) + unit_a_df['Month'].astype(str).str.zfill(2)+ unit_a_df['Day'].astype(str).str.zfill(2)
unit_a_df['Date lodged'] = pd.to_datetime(unit_a_df['dateInt'], format='%Y%m%d')

# Use the lookup table to update the risk rating
unit_a_df = pd.merge(unit_a_df,risk_df,how='inner',left_on='Rating',right_on='Risk level')

# Bring Business Unit A & B together
# tidy up A
del unit_a_df['Rating']
unit_a_df = unit_a_df.rename(columns={'Risk rating': 'Rating','Business Unit ':'Unit'})

# tidy up B
unit_b_df = unit_b_df[unit_b_df['Ticket ID'].notnull()]
unit_b_df['Ticket ID'] = unit_b_df['Ticket ID'].astype(int)
unit_b_df['Date lodged'] = pd.to_datetime(unit_b_df['Date lodged'])

# Align columns in unit A to unit B
unit_a_df = unit_a_df[unit_b_df.columns]

# concat dataframes
unit_df = pd.concat([unit_a_df,unit_b_df])

# We want to classify each case in relation to the beginning of the quarter (01/10/21):
# - Opening cases = if the case was lodged before the beginning of the quarter   
# - New cases = if the case was lodged after the beginning of the quarter
unit_df['Classification'] = np.where(unit_df['Date lodged'] < '2021-10-01','Opening cases','New cases')

# In order to count cases closed/deferred within the quarter, we want to call out cases with a completed or deferred status
# Stack Status on Classification in dataframe
unit_pivot = unit_df.melt(id_vars=['Ticket ID', 'Rating'], value_vars=['Status', 'Classification'],value_name='Values')

# Wide pivot Status Values column
unit_pivot = unit_pivot.pivot_table(values='Ticket ID', index='Rating', columns=['Values'], aggfunc='size',fill_value=0)

# clean up dataframe
unit_pivot = unit_pivot.drop(columns=['In Progress']).reset_index()

# For each rating, we then want to count how many cases are within the above 4 classifications
# We then want to create a field for Cases which will carry over into the next quarter
# - i.e. Opening Cases + New Cases - Completed Cases - Deferred Cases
unit_pivot['Continuing'] = unit_pivot['Opening cases'] + unit_pivot['New cases'] - unit_pivot['Completed'] - unit_pivot['Deferred']

# Reshape the data to match the final output
output_df = unit_pivot.melt(id_vars=['Rating'], var_name='Status', value_name='Cases')

# Output the data
# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 43 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
