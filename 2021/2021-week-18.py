# Preppin' Data 2021 Week 18
import pandas as pd
import numpy as np

# Load data
projects = pd.read_excel('unprepped_data\\PD 2021 Wk 18 Input.xlsx', engine='openpyxl', sheet_name = 'Project Timelines')

# create working dataframe
df = projects

# Workout the 'Completed Date' by adding on how many days it took to complete each task from the Scheduled Date
df['Completed Date'] = df['Scheduled Date'] + pd.to_timedelta(df['Completed In Days from Scheduled Date'],'d')

# Rename 'Completed In Days from Schedule Date' to 'Days Difference to Schedule'
df.rename(columns={'Completed In Days from Scheduled Date':'Days Difference to Schedule'}, inplace=True)

# Your workflow will likely branch into two at this point:
# 1. Pivot Task to become column headers with the Completed Date as the values in the column
# You will need to remove some data fields to ensure the result of the pivot is a single row for each project, sub-project and owner combination. 
df_1 = df[['Project','Sub-project','Owner','Task','Completed Date']]
df_1 = df_1.pivot(index=['Project','Sub-project','Owner'], columns='Task', values='Completed Date')
df_1 = df_1.reset_index()

# Calculate the difference between Scope to Build time
df_1['Scope to Build Time'] = df_1['Build'] - df_1['Scope']

# Calculate the difference between Build to Delivery time
df_1['Build to Delivery Time'] = df_1['Deliver'] - df_1['Build']

# Pivot the Build, Deliver and Scope column to re-create the 'Completed Dates' field and Task field
# You will need to rename these
df_1 = df_1.melt(id_vars=['Project','Sub-project','Owner','Scope to Build Time','Build to Delivery Time'], var_name='Task', value_name='Completed Date')

# # 2. You don't need to do anything else to this second flow
df_2 = df

# Now you will need to:
# Join Branch 1 and Branch 2 back together 
df_3 = pd.merge(df_1,df_2,  on=['Project','Sub-project','Owner','Task','Completed Date'], how='inner')

# Calculate which weekday each task got completed on as we want to know whether these are during the weekend or not for the dashboard
df_3['Completed Weekday'] = df_3['Completed Date'].dt.day_name()

# Clean up the data set to remove any fields that are not required.
df_3 = df_3[['Completed Weekday','Task','Scope to Build Time','Build to Delivery Time','Days Difference to Schedule','Project','Sub-project','Owner','Scheduled Date','Completed Date']]
df_3 = df_3.sort_values(by='Scheduled Date')

# Writing data to csv
df_3.to_csv('prepped_data\\PD 2021 Wk 18 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
