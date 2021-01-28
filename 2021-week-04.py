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

# Split the 'Customer Type - Product' field to create:
#  - Customer Type
#  - Product
#  - Also rename the Values column resulting from you pivot as 'Products Sold'


# Turn the date into a 'Quarter' number

# Sum up the products sold by Store and Quarter

# Add the Targets data

# Join the Targets data with the aggregated Stores data
#  - Note: this should give you 20 rows of data


# Remove any duplicate fields formed by the Join

# Calculate the Variance between each Store's Quarterly actual sales and the target. Call this field 'Variance to Target'

# Rank the Store's based on the Variance to Target in each quarter
#  - The greater the variance the better the rank


# Output the data

# One file:

# 6 Data Fields:

# Quarter
# Rank
# Store
# Products Sold
# Target 
# Variance to Target
# 20 Rows (21 rows including headers)
