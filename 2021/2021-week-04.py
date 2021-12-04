# Preppin' Data 2021 Week 04

import pandas as pd
import numpy as np
#from datetime import datetime

# Load Excel File tabs
manchester = pd.read_excel('unprepped_data\\PD 2021 Wk 4 Input.xlsx', engine='openpyxl', sheet_name = 'Manchester')
london = pd.read_excel('unprepped_data\\PD 2021 Wk 4 Input.xlsx', engine='openpyxl', sheet_name = 'London')
leeds = pd.read_excel('unprepped_data\\PD 2021 Wk 4 Input.xlsx', engine='openpyxl', sheet_name = 'Leeds')
york = pd.read_excel('unprepped_data\\PD 2021 Wk 4 Input.xlsx', engine='openpyxl', sheet_name = 'York')
birmingham = pd.read_excel('unprepped_data\\PD 2021 Wk 4 Input.xlsx', engine='openpyxl', sheet_name = 'Birmingham')
targets = pd.read_excel('unprepped_data\\PD 2021 Wk 4 Input.xlsx', engine='openpyxl', sheet_name = 'Targets')


# Create a Store column from the data
manchester['Store'] = 'Manchester'
london['Store'] = 'London'
leeds['Store'] = 'Leeds'
york['Store'] = 'York'
birmingham['Store'] = 'Birmingham'


# Append all tabs together
df = manchester.append(london)
df = df.append(leeds)
df = df.append(york)
df = df.append(birmingham)


# Pivot the product columns
a = df.melt(id_vars=['Date', 'Store'], 
        var_name='Customer Type - Product',
        value_name='Values')


# Split the 'Customer Type - Product' field to create:
#  - Customer Type
#  - Product
a[['Customer Type', 'Product']] = a['Customer Type - Product'].str.split(' - ',expand=True)

#  - Also rename the Values column resulting from you pivot as 'Products Sold'
a.rename(columns={'Values':'Products Sold'}, inplace=True)

# Turn the date into a 'Quarter' number
a['Date'] = pd.to_datetime(a['Date'])
a['Quarter'] = a['Date'].dt.quarter 

# Sum up the products sold by Store and Quarter
a_agg = a.groupby(['Store', 'Quarter'],as_index=False)['Products Sold'].agg('sum')

# Add the Targets data

# Join the Targets data with the aggregated Stores data
#  - Note: this should give you 20 rows of data
output = targets.merge(a_agg, on=['Store','Quarter'], how='outer')

# Remove any duplicate fields formed by the Join
output = output.drop_duplicates()

# Calculate the Variance between each Store's Quarterly actual sales and the target. Call this field 'Variance to Target'
output['Variance to Target'] = output['Products Sold'] - output['Target']


# Rank the Store's based on the Variance to Target in each quarter
#  - The greater the variance the better the rank
output['Rank'] = output.groupby('Quarter')['Variance to Target'].rank(ascending=False)
output['Rank'] = output['Rank'].astype(int)
output = output.sort_values(by=['Quarter','Rank'], ascending=[True,True]).reset_index()


# Output the data

# One file, 6 Data Fields:
# Quarter
# Rank
# Store
# Products Sold
# Target 
# Variance to Target
# 20 Rows (21 rows including headers)
output_file = output[['Quarter','Rank','Store','Products Sold','Target','Variance to Target']]
output_file.to_csv('prepped_data\\PD 2021 Wk 4 Output - Quarterly Store Sales against Targets.csv', index=False)

print("data prepped!")
