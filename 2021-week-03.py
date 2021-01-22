# Preppin' Data 2021 Week 03

import pandas as pd
import numpy as np
#from datetime import datetime

# Load Excel File tabs
manchester = pd.read_excel('unprepped_data\\PD 2021 Wk 3 Input.xlsx', engine='openpyxl', sheet_name = 'Manchester')
london = pd.read_excel('unprepped_data\\PD 2021 Wk 3 Input.xlsx', engine='openpyxl', sheet_name = 'London')
leeds = pd.read_excel('unprepped_data\\PD 2021 Wk 3 Input.xlsx', engine='openpyxl', sheet_name = 'Leeds')
york = pd.read_excel('unprepped_data\\PD 2021 Wk 3 Input.xlsx', engine='openpyxl', sheet_name = 'York')
birmingham = pd.read_excel('unprepped_data\\PD 2021 Wk 3 Input.xlsx', engine='openpyxl', sheet_name = 'Birmingham')

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

# Pivot 'New' and 'Existing' columns
a = df.melt(id_vars=['Date', 'Store'], 
        var_name='Customer Type - Product',
        value_name='Values')

# Split the former column headers to form: Customer Type and Product
a[['Customer Type', 'Product']] = a['Customer Type - Product'].str.split(' - ',expand=True)


# Rename the measure created by the Pivot as 'Products Sold'
a.rename(columns={'Values':'Products Sold'}, inplace=True)

# Turn Date into Quarter
a['Date'] = pd.to_datetime(a['Date'])
a['Quarter'] = a['Date'].dt.quarter 

# Aggregate to form two separate outputs of the number of products sold by:
# 1. Product, Quarter
output_1 = a.groupby(['Product', 'Quarter'],as_index=False)['Products Sold'].agg('sum')

# 2. Store, Customer Type, Product
output_2 = a.groupby(['Store', 'Customer Type','Product'],as_index=False)['Products Sold'].agg('sum')

# Output each data set as a csv
output_1.to_csv('prepped_data\\PD 2021 Wk 3 Output - 1 Sales by Product and Quarter.csv', index=False)
output_2.to_csv('prepped_data\\PD 2021 Wk 3 Output - 2 Sales by Store Cust Type and Product.csv', index=False)

print("data prepped!")
