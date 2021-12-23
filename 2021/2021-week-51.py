import pandas as pd
import numpy as np

# Load Data
df = pd.read_csv('unprepped_data\\PD 2021 Wk 51 Input.csv')

# Split out the store name from the OrderID
df[['Store', 'OrderID']] = df['OrderID'].str.split('-', 1, expand=True)

# Turn the Return State field into a binary Returned field
df['Returned'] = np.where(df['Return State'].isnull(),False,True)

# Create a Sales field
df['Sales'] = pd.to_numeric(df['Unit Price'].str.replace('£',''), downcast='float')*df['Quantity']

# Create 3 dimension tables for Store, Customer and Product
#  - When assigning IDs, these should be created using the dimension and minimum order date fields so that the IDs do not change when later orders are placed
#  - For the Customer dimension table, we want to include additional fields detailing their total number of orders and the % of products they have returned
store_df = df[['Store','Order Date']]
store_df = store_df.groupby(['Store']).agg(first_order=('Order Date','min')).reset_index()
store_df.rename(columns={'first_order':'First Order'}, inplace=True)
store_df['StoreID'] = store_df.index + 1
store_df = store_df[['StoreID','Store','First Order']]

customer_df = df[['Customer','Returned','OrderID','Order Date']]
customer_df['Returned Orders'] = np.where(customer_df['Returned'],1,0)
customer_df = customer_df.groupby(['Customer']).agg(returns=('Returned Orders','sum'),orders=('OrderID','count'),first_order=('Order Date','min')).reset_index()
customer_df['Return %'] = customer_df['returns']/customer_df['orders']
customer_df.rename(columns={'first_order':'First Order','orders':'Number of Orders'}, inplace=True)
customer_df['CustomerID'] = customer_df.index + 1
del customer_df['returns']
customer_df = customer_df[['CustomerID','Customer','Return %','Number of Orders','First Order']]

product_df = df[['Product Name','Sub-Category','Category','Unit Price','Order Date']]
product_df = product_df.groupby(['Product Name','Sub-Category','Category','Unit Price']).agg(first_order=('Order Date','min')).reset_index()
product_df.rename(columns={'first_order':'First Sold'}, inplace=True)
product_df['ProductID'] = product_df.index + 1
product_df = product_df[['ProductID','Category','Sub-Category','Product Name','Unit Price','First Sold']]

# Replace the dimensions with their IDs in the original dataset to create the fact table
fact_df = pd.merge(df,store_df,on=['Store'],how='inner')
fact_df = pd.merge(fact_df,customer_df,on=['Customer'],how='inner')
fact_df = pd.merge(fact_df,product_df,on=['Product Name','Sub-Category','Category','Unit Price'],how='inner')

# reduce columns
fact_cols = ['StoreID','CustomerID','OrderID','Order Date','ProductID','Returned','Quantity','Sales']
fact_df = fact_df[fact_cols]

# Output the fact and dimension tables
# Writing data to csv
fact_df.to_csv('prepped_data\\PD 2021 Wk 51 Output - fact table.csv', encoding='utf-8-sig', index=False)
store_df.to_csv('prepped_data\\PD 2021 Wk 51 Output - store table.csv', encoding='utf-8-sig', index=False)
customer_df.to_csv('prepped_data\\PD 2021 Wk 51 Output - customer table.csv', encoding='utf-8-sig', index=False)
product_df.to_csv('prepped_data\\PD 2021 Wk 51 Output - product table.csv', encoding='utf-8-sig', index=False)

print("data prepped!")
