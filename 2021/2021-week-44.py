# Preppin' Data 2021 Week 44
import pandas as pd
import numpy as np

# Load data
df = pd.read_excel('unprepped_data\\PD 2021 Wk 44 Input.xlsx', sheet_name='Raw data')

# Convert the Value field to just be Kilometres ridden 
#  - Carl cycles at an average of 30 kilometres per hour whenever he is measuring his sessions in minutes
df['km'] = np.where(df['Measure'] == 'min',(df['Value']/60)*30,df['Value'])

# Create a field called measure to convert KM measurements into 'Outdoors' and any measurement in 'mins' as 'Turbo Trainer'.
df['location'] = np.where(df['Measure'] == 'min','Outdoors','Turbo Trainer')

# Create a separate column for Outdoors and Turbo Trainer (indoor static bike values
df['Outdoors'] = np.where(df['location'] == 'Outdoors',df['km'],0)
df['Turbo Trainer'] = np.where(df['location'] == 'Turbo Trainer',df['km'],0)

# Ensure there is a row for each date between 1st Jan 2021 and 1st Nov 2021(inclusive)
# build a data frame of all dates from min to max
min_date = '2021-01-01'
max_date = '2021-11-01'
idx = pd.date_range(min_date, max_date)

all_dates = pd.DataFrame()
all_dates['Date'] = idx 
# dt.normalize() to remove time component and keep as date type
all_dates['Date'] = all_dates['Date'].dt.normalize()

df = pd.merge(all_dates,df,on = 'Date', how = 'left')

# Count the number of activities per day and work out the total distance cycled Outdoors or on the Turbo Trainer
# Change any null values to zero
df['Outdoors'] = df['Outdoors'].fillna(0)
df['Turbo Trainer'] = df['Turbo Trainer'].fillna(0)

df = df.groupby(['Date']).agg(activities = ('km','count'),outdoors = ('Outdoors','sum'),turbo = ('Turbo Trainer','sum')).reset_index()

# Work out how many days I did no activities
no_act_df = df.loc[df['activities'] == 0]
days_of_no_activities = len(no_act_df)

print('No activities on ' + str(days_of_no_activities) + ' days')

# Output a file to help me explore the analysis further

# Reorder and rename columns
df = df[['Date','activities','turbo','outdoors']]
df.columns = ['Date','Activites per day','Turbo Trainer','Outdoors']

# Write to csv
df.to_csv('prepped_data\\PD 2021 Wk 44 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
