# Preppin' Data 2021 Week 33
import pandas as pd
import numpy as np

# Load data
# Create one complete data set
# Read all Excel tabs and concat as one dateframe
all_tabs = pd.read_excel('unprepped_data\\PD 2021 Wk 33 Input.xlsx', sheet_name=None)

# Bring all the sheets together
# Use the Table Names field to create the Reporting Date
all_dfs = []
for tab_name, df in all_tabs.items():
    df['Reporting Date'] = tab_name
    all_dfs.append(df)
    orders_df = pd.concat(all_dfs, ignore_index=True)

orders_df['Sale Date'] = pd.to_datetime(orders_df['Sale Date'])
orders_df['Reporting Date'] = pd.to_datetime(orders_df['Reporting Date'],format = "%Y%m%d")

# Find the Minimum and Maximum date where an order appeared in the reports
min_date = orders_df.groupby(['Orders']).agg(min_date = ('Reporting Date','min')).reset_index()
max_date = orders_df.groupby(['Orders']).agg(max_date = ('Reporting Date','max')).reset_index()

# add min and max date as new columns
orders_df = pd.merge(orders_df,min_date,on='Orders', how='inner')
orders_df = pd.merge(orders_df,max_date,on='Orders', how='inner')

# Add one week on to the maximum date to show when an order was fulfilled by
orders_df['fulfilled by'] = orders_df['max_date'] + pd.DateOffset(days=7)

# Apply this logic:
#  - The first time an order appears it should be classified as a 'New Order'
#  - The week after the last time an order appears in a report (the maximum date) is when the order is classed as 'Fulfilled' 
#  - Any week between 'New Order' and 'Fulfilled' status is classed as an 'Unfulfilled Order' 

orders_df['Order Status'] = np.where(orders_df['Reporting Date']==orders_df['min_date'],'New Order','Unfulfilled Order')

# create data set of when orders where fulfilled (not in original data set)
fulfilled_orders = orders_df[['Orders','Sale Date','fulfilled by']].drop_duplicates()
fulfilled_orders['Order Status'] = 'Fulfilled'
fulfilled_orders = fulfilled_orders.rename(columns={'fulfilled by':'Reporting Date'})

# filter out future reporting dates
max_report_date = max(orders_df['Reporting Date'])
fulfilled_orders = fulfilled_orders.loc[fulfilled_orders['Reporting Date'] <= max_report_date]

# Pull of the data sets together 
# Remove any unnecessary fields
orders_df = orders_df[fulfilled_orders.columns]
output_df = orders_df.append(fulfilled_orders, ignore_index=True)

# Output the data
output_df = output_df.sort_values(by=['Orders','Sale Date'])
output_df.to_csv('prepped_data\\PD 2021 Wk 33 Output.csv', index=False)

print("data prepped!")
