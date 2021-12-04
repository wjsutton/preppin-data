# Preppin' Data 2021 Week 02

import pandas as pd
import numpy as np
from datetime import datetime

# Load csv
df = pd.read_csv('unprepped_data\\PD 2021 Wk 2 Input - Bike Model Sales.csv')

# Clean up the Model field to leave only the letters to represent the Brand of the bike
df['Model'] = df['Model'].str.extract(r'([a-zA-Z]+)')

# Workout the Order Value using Value per Bike and Quantity
df['Order Value'] = df['Quantity'] * df['Value per Bike']

# Aggregate Value per Bike, Order Value and Quantity by Brand and Bike Type to form:
# - Quantity Sold
# - Order Value
# - Average Value Sold per Brand, Type
a = df.groupby(
     ['Model','Bike Type']
 ).agg(
     Quantity_Sold = ('Quantity','sum'),
     Order_Value = ('Order Value','sum'),
 ).reset_index()

a['Average Value Sold'] = a['Order_Value'] / a['Quantity_Sold']

# Calculate Days to ship by measuring the difference between when an order was placed and when it was shipped as 'Days to Ship'
df['Shipping Date'] = pd.to_datetime(df['Shipping Date'], format="%d/%m/%Y")
df['Order Date'] = pd.to_datetime(df['Order Date'], format="%d/%m/%Y")

df['Days to Ship'] = df['Shipping Date'].sub(df['Order Date'], axis=0)
df['Days to Ship'] = df['Days to Ship']/ np.timedelta64(1, 'D')

# Aggregate Order Value, Quantity and Days to Ship by Brand and Store to form:
# - Total Quantity Sold
# - Total Order Value
# - Average Days to Ship
b = df.groupby(
     ['Model','Store']
 ).agg(
     Total_Quantity_Sold = ('Quantity','sum'),
     Total_Order_Value = ('Order Value','sum'),
     Average_Days_to_Ship = ('Days to Ship','mean'),
 ).reset_index()

# Round any averaged values to one decimal place to make the values easier to read
a['Average Value Sold'] = a['Average Value Sold'].round(1)
b['Average_Days_to_Ship'] = b['Average_Days_to_Ship'].round(1)

# Output two files as csvs

# File 1. Sales by Brand and Type
# 5 Data Fields: Brand, Bike Type, Quantity Sold, Order Value, Avg Bike Value per Brand
# 15 Rows (16 including headers)

# renaming columns
new_a_columns = a.columns.values
new_a_columns = ['Brand', 'Bike Type', 'Quantity Sold', 'Order Value', 'Avg Bike Value per Brand']
a.columns  = new_a_columns

# writing data to csv
a.to_csv('prepped_data\\PD 2021 Wk 2 Output - 1 Sales by Brand and Type.csv', index=False)

# File 2. Sales by Brand and Store
# 5 Data Fields: Brand, Store, Total Quantity Sold, Total Order Value, Avg Days to Ship
# 25 Rows (26 including headers)

# renaming columns
new_b_columns = b.columns.values
new_b_columns = ['Brand', 'Store', 'Total Quantity Sold', 'Total Order Value', 'Avg Days to Ship']
b.columns  = new_b_columns

# writing data to csv
b.to_csv('prepped_data\\PD 2021 Wk 2 Output - 2 Sales by Brand and Store.csv', index=False)

print("data prepped!")
