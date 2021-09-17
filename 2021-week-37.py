# Preppin' Data 2021 Week 37
import pandas as pd
import numpy as np

# Load data
contract_df = pd.read_excel('unprepped_data\\PD 2021 Wk 37 Input.xlsx', sheet_name='Contract Details')
scaffold_df = pd.read_excel('unprepped_data\\PD 2021 Wk 37 Input.xlsx', sheet_name='Scaffold')

# Calculate the End Date for each contract
contract_df['Start Date'] = pd.to_datetime(contract_df['Start Date'], format="Y-m-d")

# Add Calendar Month:
# Take Start Date month, add contract months, then add Start Date day and subtrack 1 day
contract_df['End Date'] = contract_df['Start Date'].values.astype('datetime64[M]') + contract_df['Contract Length (months)'].values.astype('timedelta64[M]') + contract_df['Start Date'].dt.day.apply(pd.offsets.Day)  - pd.DateOffset(days=1)

# Create a Row for each month a person will hold the contract
names = contract_df['Name']
months = contract_df['Contract Length (months)']

name_output = []
month_output = []

# Create loop that cycles through names creating 2 lists:
# - 1. The person's name repeated for the number of contract months
# - 2. The contract month number 0 to final month -1 
for i in range(len(names)):
    name_output = name_output + [names[i]]*months[i]
    month_output = month_output + list(range(0,months[i]))

# Write lists to dataframe and join to original dataset so there is 1 row per person and month
loop_df = pd.DataFrame(list(zip(name_output,month_output)),columns=['Name','Month Number'])
output_df = pd.merge(contract_df,loop_df,how='inner',on='Name')

# Calculate the monthly cumulative cost of each person's contract
output_df['Cumulative Monthly Cost'] = output_df['Monthly Cost'] * output_df['Month Number']

# Add Calendar Month:
# Take Start Date month, add contract months, then add Start Date day and subtrack 1 day
output_df['Payment Date'] = output_df['Start Date'].values.astype('datetime64[M]') + output_df['Month Number'].values.astype("timedelta64[M]") + output_df['Start Date'].dt.day.apply(pd.offsets.Day)  - pd.DateOffset(days=1)

# Output the Data
columns = ['Name','Payment Date','Monthly Cost','Cumulative Monthly Cost']
output_df = output_df[columns]

# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 37 Output.csv', index=False)

print("data prepped!")
