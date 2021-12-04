# Preppin' Data 2021 Week 15
import pandas as pd
import numpy as np

# Load data
menu = pd.read_excel('unprepped_data\\PD 2021 Wk 15 Input - Menu and Orders.xlsx', engine='openpyxl', sheet_name = 'MENU')
order = pd.read_excel('unprepped_data\\PD 2021 Wk 15 Input - Menu and Orders.xlsx', engine='openpyxl', sheet_name = 'Order')

# Modify the structure of the Menu table so we can have one column for:
#  - the Type (pizza, pasta, house plate), 
#  - the name of the plate, 
#  - ID, and Price

# reduce to individual data frames
pizza = menu.loc[:, 'Pizza':'Pizza ID']
pasta = menu.loc[:, 'Pasta':'Pasta ID']
house_plates = menu.loc[:, 'House Plates':'House Plates ID']

# rename all columns
columns = ['Plate','Price','ID']

pizza.columns = columns
pasta.columns = columns
house_plates.columns = columns

# add food type
pizza['Type'] = 'Pizza'
pasta['Type'] = 'Pasta'
house_plates['Type'] = 'House Plates'

# concat all data frames and remove NaNs
menu_df = pd.concat([pizza,pasta,house_plates])
menu_df = menu_df[menu_df.ID.notnull()]

# Modify the structure of the Orders table to have each item ID in a different row 

order['ID'] = order.index

# split string into seperate columns
a = pd.DataFrame(order['Order'].str.split('-',expand=True), index=order['ID'])

a.columns = ['1','2','3','4']
a['ID'] = a.index

# seperate into 2 column dataframes
a1 = a[['ID','1']]
a2 = a[['ID','2']]
a3 = a[['ID','3']]
a4 = a[['ID','4']]

 # rename all columns
a1.columns = ['ID','Order ID']
a2.columns = a1.columns
a3.columns = a1.columns
a4.columns = a1.columns

# stack dataframes and remove null entries
order_ids = pd.concat([a1,a2,a3,a4])
order_ids = order_ids[order_ids['Order ID'].notnull()]
del order_ids['ID']

# join back to original orders table and delete unused columns
order_df = pd.merge(order,order_ids, on='ID', how = 'left')
order_df['Order ID'] = np.where(order_df['Order ID'].notnull(), order_df['Order ID'], order_df['Order'])
del order_df['Order']
del order_df['ID']

# Join both tables 

# convert join columns to int
order_df = order_df.astype({'Order ID': int})
menu_df = menu_df.astype({'ID': int})

# join menu with orders
takings_df = pd.merge(menu_df, order_df, left_on='ID', right_on='Order ID', how='left')

# On Monday's we offer a 50% discount on all items. Recalculate the prices to reflect this
# work out weekday and apply discount
takings_df['weekday'] = takings_df['Order Date'].dt.dayofweek
# Note Mondays are denoted as 0
takings_df['Price Paid'] = np.where(takings_df['weekday'] == 0 , takings_df['Price']/2, takings_df['Price'])

# convert weekday to day name
takings_df['weekday'] = np.select(
    [
        takings_df['weekday'] == 0, 
        takings_df['weekday'] == 1,
        takings_df['weekday'] == 2, 
        takings_df['weekday'] == 3,
        takings_df['weekday'] == 4, 
        takings_df['weekday'] == 5,
        takings_df['weekday'] == 6
    ], 
    [
        'Monday', 
        'Tuesday',
        'Wednesday', 
        'Thursday',
        'Friday', 
        'Saturday',
        'Sunday'
    ], 
    default='Unknown'
)
#print(takings_df)

# For Output 1, we want to calculate the total money for each day of the week 
output_1 = takings_df[['weekday','Price Paid']]
output_1 = output_1.groupby(['weekday']).sum()

# For Output 2, we want to reward the customer who has made the most orders for their loyalty. 
# Work out which customer has ordered the most single items.
output_2 = takings_df[['Customer Name','Order ID']]
output_2 = output_2.groupby(['Customer Name']).agg('count')

max_orders = output_2['Order ID'].max()
output_2 = output_2.loc[output_2['Order ID'] == max_orders]
output_2.columns = ['Count Items']

# Writing data to csv
output_1.to_csv('prepped_data\\PD 2021 Wk 15 Output - Weekday Sales.csv', index=True)
output_2.to_csv('prepped_data\\PD 2021 Wk 15 Output - Top Customer.csv', index=True)

print("data prepped!")
