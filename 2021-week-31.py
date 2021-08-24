# Preppin' Data 2021 Week 31
import pandas as pd
import numpy as np

# Load data
bike_df = pd.read_csv('unprepped_data\\PD 2021 Wk 31 Input.csv')

# Remove the 'Return to Manufacturer' records
bike_df = bike_df.loc[bike_df['Status'] != 'Return to Manufacturer']

# Create a total for each Store of all the items sold
store_sales = bike_df.groupby(['Store']).agg(total_sales = ('Number of Items','sum')).reset_index()

# Aggregate the data to Store sales by Item
item_sales = bike_df.groupby(['Store','Item']).agg(sales = ('Number of Items','sum')).reset_index()

# Pivot item sales
item_pivot = item_sales.pivot(index='Store', columns='Item', values='sales')

# Merge pivot table and store sales
output_df = pd.merge(item_pivot,store_sales,on='Store',how='inner')

# Prep output table
output_df = output_df.rename(columns={'total_sales':'Items sold per store'})
output_df = output_df[['Items sold per store','Wheels','Tyres','Saddles','Brakes','Store']]

# Output the data
output_df.to_csv('prepped_data\\PD 2021 Wk 31 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
