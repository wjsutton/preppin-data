# Preppin' Data 2021 Week 24
import pandas as pd
import numpy as np
from datetime import date, timedelta

# Load data
reasons = pd.read_excel('unprepped_data\\PD 2021 Wk 24 Input - Absenteeism Scaffold.xlsx', sheet_name='Reasons')
scaffold = pd.read_excel('unprepped_data\\PD 2021 Wk 24 Input - Absenteeism Scaffold.xlsx', sheet_name='Scaffold')

# Build a data set that has each date listed out between 1st April to 31st May 2021
sdate = date(2021,4,1)   # start date
edate = date(2021,5,31)   # end date

# make list of dates and add to dataframe
apr_to_may = pd.date_range(sdate,edate,freq='d')
apr_to_may_df = pd.DataFrame()
apr_to_may_df['Date'] = apr_to_may

# Build a data set containing each date someone will be off work
# loop through absentees and create date range
for i in range(len(reasons)):
    sdate = reasons['Start Date'][i]
    edate = reasons['Start Date'][i] + timedelta(days=np.float64(reasons['Days Off'][i]))
    off_range = pd.date_range(sdate,edate-timedelta(days=1),freq='d')

    off_work = pd.DataFrame()
    off_work['Date'] = off_range
    off_work['Name'] = reasons['Name'][i]

    if i == 0:
        off_work_df = off_work
    
    if i > 0:
        off_work_df = pd.concat([off_work_df,off_work])

# Merge these two data sets together 
sickness_df = pd.merge(apr_to_may_df,off_work_df, on = 'Date', how = 'left')

# Workout the number of people off each day
output_df = sickness_df.groupby(['Date'],as_index=False).count()

# Output the data
column_names = ['Date','Number of people off each day']
output_df.columns = column_names
output_df.to_csv('prepped_data\\PD 2021 Wk 24 Output.csv', encoding="utf-8-sig", index=False)


# Can you answer:
# - What date had the most people off?
max_sickness = output_df.loc[output_df['Number of people off each day'] == max(output_df['Number of people off each day'])]
print('What date had the most people off?')
print(max_sickness['Date'])

# - How many days does no-one have time off on?
full_house = output_df.loc[output_df['Number of people off each day'] == 0]
print('How many days does no-one have time off on?')
print(len(full_house))

print("data prepped!")
