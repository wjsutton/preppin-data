# Preppin' Data 2021 Week 50
import pandas as pd
import numpy as np

# Load Data
oct_df = pd.read_excel('unprepped_data\\PD 2021 Wk 50 Input.xlsx', engine='openpyxl', sheet_name = 'October')
nov_df = pd.read_excel('unprepped_data\\PD 2021 Wk 50 Input.xlsx', engine='openpyxl', sheet_name = 'November')

# Fill in the Salesperson names for each row (the name appears at the bottom of each monthly grouping)
# use 'bfill' method to backfill null columns with next value that isn't null
oct_df['Salesperson'] = oct_df['Salesperson'].fillna(method='bfill')
nov_df['Salesperson'] = nov_df['Salesperson'].fillna(method='bfill')

# Bring out the YTD information from the October tracker and use it to create YTD totals for November too
oct_df.rename( columns={'Unnamed: 7':'YTD Total'}, inplace=True )
oct_df['YTD Total'] = oct_df['YTD Total'].fillna(method='bfill')
oct_df = oct_df.loc[oct_df['Total'] != 'YTD total:']

nov_df = nov_df[nov_df['Total'].notnull()]
nov_ytd = nov_df.groupby(['Salesperson']).agg(ytd_total=('Total','sum')).reset_index()
nov_ytd.columns = ['Salesperson','YTD Total']
nov_df = pd.merge(nov_df,nov_ytd,on='Salesperson', how='inner')

# concat data frames
bike_df = pd.concat([oct_df,nov_df])

# Reshape the data so all the bike types are in a single column
# unpivot dataset with melt function
bike_pivot = pd.melt(bike_df, id_vars=['RowID','Date','Salesperson','Total','YTD Total'], var_name='Bike Type',value_name='Sales')

# Output the data
cols = ['Salesperson','Date','Bike Type','Sales','YTD Total']
bike_pivot = bike_pivot[cols]

# Writing data to csv
bike_pivot.to_csv('prepped_data\\PD 2021 Wk 50 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
