# Preppin' Data 2021 Week 26
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime 

# Load data
rolling = pd.read_csv('unprepped_data\\PD 2021 Wk 26 Input - Sheet1.csv')

# Create a data set that gives 7 rows per date (unless those dates aren't included in the data set). 
# - ie 1st Jan only has 4 rows of data (1st, 2nd, 3rd & 4th)

dates = list(set(list(rolling['Date'])))
number_of_dates = len(dates)

# loop through each date, find the 3 days before, 3 after
# create a dataframe and concat together
for i in range(number_of_dates):
    a = dates[i]
    b = datetime.strptime(a, '%d/%m/%Y')

    sdate = b-timedelta(days=3)
    edate = b+timedelta(days=3)
    rolling_days = pd.date_range(sdate,edate,freq='d')
    
    # make list of dates and add to dataframe
    rolling_days_entry = pd.DataFrame()

    rolling_days_entry['Rolling Dates'] = rolling_days
    rolling_days_entry['Date'] = a
    rolling_days_entry['Date Formatted'] = b

    if i == 0:
        rolling_days_df = rolling_days_entry

    if i > 0:
        rolling_days_df = pd.concat([rolling_days_df,rolling_days_entry])

# create join column and merge to existing dataframe
rolling_days_df['Rolling Dates Join'] = rolling_days_df['Rolling Dates'].dt.strftime('%d/%m/%Y')
rolling_df = pd.merge(rolling,rolling_days_df,left_on='Date',right_on = 'Rolling Dates Join',how='inner')

# Remove any additional fields you don't need 
roll_df = rolling_df[['Destination','Date_y','Revenue']]
roll_df.columns = ['Destination','Date','Revenue']

# Create the Rolling Week Total and Rolling Week Average per destination
# Records that have less than 7 days data should remain included in the output
# Create the Rolling Week Total and Rolling Week Average for the whole data set
# Pull the data together for the previous two requirements

# create total and concat to destination dataframe
total_df = roll_df.copy() 
total_df['Destination'] = 'All' 
output = pd.concat([roll_df,total_df])

# Create the Rolling Week Total and Rolling Week Average for the whole data set
output = output.groupby(['Destination','Date'],as_index=False)['Revenue'].agg({'Rolling Week Total': 'sum'})
output['Rolling Week Avg'] = output['Rolling Week Total']/7

# Output the data, reorder columns and write to csv
output = output[['Destination','Date','Rolling Week Avg','Rolling Week Total']]
output.to_csv('prepped_data\\PD 2021 Wk 26 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
