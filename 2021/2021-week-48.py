# Preppin' Data 2021 Week 48
import pandas as pd
import numpy as np

# Load data
# Extract each data table within the Excel workbook
lewisham = pd.read_excel('unprepped_data\\PD 2021 Wk 48 Input.xlsx', engine='openpyxl', sheet_name='Sheet1',nrows= 3,skiprows = 1, usecols = "B:D")
wimbledon = pd.read_excel('unprepped_data\\PD 2021 Wk 48 Input.xlsx', engine='openpyxl', sheet_name='Sheet1',nrows= 3,skiprows = range(1,7), usecols = "B:D")
wimbledon_header = pd.read_excel('unprepped_data\\PD 2021 Wk 48 Input.xlsx', engine='openpyxl', sheet_name='Sheet1',nrows= 1,skiprows = range(1,6), usecols = "B:D")
york = pd.read_excel('unprepped_data\\PD 2021 Wk 48 Input.xlsx', engine='openpyxl', sheet_name='Sheet1',nrows= 4,skiprows = range(1,12), usecols = "B:D")
york_header = pd.read_excel('unprepped_data\\PD 2021 Wk 48 Input.xlsx', engine='openpyxl', sheet_name='Sheet1',nrows= 1,skiprows = range(1,11), usecols = "B:D")

# Extract the branch name from the table structure
lewisham['Branch'] = lewisham.columns[0]
wimbledon['Branch'] = wimbledon_header.iat[0,0]
york['Branch'] = york_header.iat[0,0]

cols = ['Metric','2020','2021','Branch']

lewisham.columns = cols
wimbledon.columns = cols
york.columns = cols

branch_df = pd.concat([lewisham,wimbledon,york])

# Create a row per measure and year
# Remove the word 'Year' from the year values
branch_pivot = pd.melt(branch_df, id_vars=['Metric','Branch'], var_name='Recorded Year',value_name='Value')

# Create a True Value (i.e. the correct number of zeros for the measure)
branch_pivot['True Value'] = np.where(branch_pivot['Metric'].str.contains('(k)', regex=False),branch_pivot['Value']*1000,np.where(branch_pivot['Metric'].str.contains('(m)', regex=False),branch_pivot['Value']*1000000,branch_pivot['Value']))

# Remove the suffix of the measure (i.e. the (k) or (m) if the measure name has the units)
branch_pivot['Clean Measure names'] = branch_pivot['Metric'].replace(" \(m\)| \(k\)", "", regex=True) 

# Remove unneeded columns
output_cols = ['Branch','Clean Measure names','Recorded Year','True Value']
output_df = branch_pivot[output_cols]

# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 48 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
