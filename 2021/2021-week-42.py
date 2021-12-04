# Preppin' Data 2021 Week 42
import pandas as pd
import numpy as np

# Input the data
df = pd.read_csv('unprepped_data\\PD 2021 Wk 42 Input.csv')

# Create new rows for any date missing between the first and last date in the data set provided
# build a data frame of all dates from min to max
min_date = min(df['Date'])
max_date = max(df['Date'])
idx = pd.date_range(min_date, max_date)

all_dates = pd.DataFrame()
all_dates['Date'] = idx 
# dt.normalize() to remove time component and keep as date type
all_dates['Date'] = all_dates['Date'].dt.normalize()

# merge all_dates with original dataframe, 
df['Date'] = pd.to_datetime(df['Date'], format='%d/%M/%Y').dt.normalize()
df = pd.merge(all_dates,df,on='Date',how='left')

# fillna(method='pad') always NANs to be replaced with previous row's value
df['Total Raised to date'] = df['Total Raised to date'].fillna(method='pad')

# Calculate how many days of fundraising there has been by the date in each row (1st Jan would be 0)
df['Days into fund raising'] = range(0, len(idx))

# Calculate the amount raised per day of fundraising for each row
df['Value raised per day'] = df['Total Raised to date'] / df['Days into fund raising']

# Workout the weekday for each date
df['Day of week'] = df['Date'].dt.day_name()

# Average the amount raised per day of fundraising for each weekday
df['Avg raised per weekday'] = df['Value raised per day'].groupby(df['Day of week']).transform('mean')

# Output the data
cols = ['Day of week','Total Raised to date','Days into fund raising','Value raised per day','Avg raised per weekday']
df = df[cols]
df = df.rename(columns={'Day of week': 'Date'})

# Write to csv
df.to_csv('prepped_data\\PD 2021 Wk 42 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
