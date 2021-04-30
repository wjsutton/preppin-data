# Preppin' Data 2021 Week 17
import pandas as pd
import numpy as np

# Load data
employee_log = pd.read_excel('unprepped_data\\PD 2021 Wk 17 Input - Preppin Data Challenge.xlsx', engine='openpyxl', sheet_name = 'Sheet1')

# Remove the ‘Totals’ Rows
employee_df = employee_log.loc[employee_log['Name, Age, Area of Work'].notnull()]
employee_df = employee_df.dropna(how='all', axis='columns')

# Pivot Dates to rows and rename fields 'Date' and 'Hours'
employee_df = employee_df.melt(id_vars=['Name, Age, Area of Work','Project'], var_name='Date', value_name='Hours')

# Split the ‘Name, Age, Area of Work’ field into 3 Fields and Rename
employee_df[['Name', 'Age, Area of Work']] = employee_df['Name, Age, Area of Work'].str.split(', ',expand=True)
employee_df[['Age', 'Area of Work']] = employee_df['Age, Area of Work'].str.split(': ',expand=True)

# Remove unnecessary fields
cols = ['Name, Age, Area of Work', 'Age, Area of Work']
employee_df = employee_df.drop(cols, 1)

# Remove the row where Dan was on Annual Leave and check the data type of the Hours Field.
employee_df = employee_df.loc[employee_df['Hours'] != 'Annual Leave']
employee_df['Hours'] = employee_df['Hours'].astype(float)
employee_df = employee_df[employee_df['Hours'].notnull()]

# Total up the number of hours spent on each area of work for each date by each employee.
output = employee_df.groupby(['Area of Work','Date','Name'], as_index=False).sum('Hours')

# First we are going to work out the avg number of hours per day worked by each employee
# Calculate the total number of hours worked and days worked per person
# Calculate the avg hours and remove unnecessary fields.
total_hours = employee_df.groupby('Name', as_index=False).sum('Hours')
total_days = employee_df.groupby('Name', as_index=False)['Date'].nunique()

total_df = pd.merge(total_days,total_hours, on='Name', how = 'inner')
total_df['Avg Number of Hours worked per day'] = total_df['Hours']/total_df['Date']

# Dropping columns
cols = ['Date', 'Hours']
total_df = total_df.drop(cols, 1)

# Now we are going to work out what % of their day (not including Chats) was spend on Client work.

# Filter out Work related to Chats.
output = output.loc[output['Area of Work'] != 'Chats']

# Calculate total number of hours spent working on each area for each employee
total_hours_exc_chats = output.groupby('Name', as_index=False).sum('Hours')

# Calculate total number of hours spent working on both areas together for each employee
client_work_df = output.loc[output['Area of Work'] == 'Client']
client_work_hours = client_work_df.groupby('Name', as_index=False).sum('Hours')
client_work_hours.columns = ['Name','Client Hours']

# Calculate the % of total and remove unnecessary fields
client_hours_df = pd.merge(client_work_hours,total_hours_exc_chats, on='Name', how = 'inner')
client_hours_df['% of Total'] = client_hours_df['Client Hours'] / client_hours_df['Hours']

# Dropping columns
cols = ['Client Hours', 'Hours']
client_hours_df = client_hours_df.drop(cols, 1)

# Join to the table with Avg hours to create your final output
output_df = pd.merge(client_hours_df,total_df, on='Name', how = 'inner')
output_df['Area of Work'] = 'Client'

# Output the data
output_df = output_df[['Name','Area of Work','% of Total','Avg Number of Hours worked per day']]

# Writing data to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 17 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")