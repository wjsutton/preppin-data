# Preppin' Data 2021 Week 09
import pandas as pd

# Load data
area_codes = pd.read_excel('unprepped_data\\PD 2021 Wk 9 Input - Area Code Lookup.xlsx', engine='openpyxl', sheet_name = 'Sheet1')
customer_info = pd.read_excel('unprepped_data\\PD 2021 Wk 9 Input - Customer Information.xlsx', engine='openpyxl', sheet_name = 'Sheet1')
product_lookup = pd.read_excel('unprepped_data\\PD 2021 Wk 9 Input - Product Lookup.xlsx', engine='openpyxl', sheet_name = 'Sheet1')

# Input the Customer Information file, split the values and reshape the data so there is a separate ID on each row.
ids = customer_info['IDs'].str.split(' ')
ids = ids.explode('IDs')
df = pd.DataFrame()
df['IDs'] = ids

# Each ID field contains the following information we need to extract: 
# - The first 6 digits present in each ID is the customers phone number
df['Customer Phone Number'] = df['IDs'].str.extract(r'(\d{6})')

# - The first 2 digits after the ‘,’ is the last 2 digits of the area code 
df['Area Code'] = df['IDs'].str.extract(r'(,\d{2})')
df['Area Code'] = df['Area Code'].str.extract(r'(\d{2})')

# - The letter following this is the first letter of the name of the area that they are calling from
df['Area Name'] = df['IDs'].str.extract(r'(,\d{2}[A-Z]{1})')
df['Area Name'] = df['Area Name'].str.extract(r'([A-Z]{1})')

# - The digits after this letter resemble the quantity of products ordered
df['Quantity'] = df['IDs'].str.extract(r'(,\d{2}[A-Z]{1}\d+)')
df['Quantity'] = df['Quantity'].str.extract(r'([A-Z]{1}\d+)')
df['Quantity'] = df['Quantity'].str.extract(r'(\d+)')

# - The letters after the ‘-‘ are the product ID codes 
df['Product Code'] = df['IDs'].str.extract(r'(-[A-Z]+)')
df['Product Code'] = df['Product Code'].str.extract(r'([A-Z]+)')

# Rename these fields appropriately, and remove any unwanted columns – leaving only these 5 columns in the workflow.
df = df[['Customer Phone Number','Area Code','Area Name','Quantity','Product Code']]
 
# Input the Area Code Lookup Table – find a way to join it to the Customer information file 
area_codes['Last 2'] = area_codes['Code'].astype(str).str[-2:]
area_codes['Letter'] = area_codes['Area'].str[0]
output = pd.merge(df, area_codes, left_on=['Area Code','Area Name'], right_on=['Last 2','Letter'])

# We don’t actually sell products in Clevedon, Fakenham, or Stornoway. Exclude these from our dataset 
no_sell = ['Clevedon', 'Fakenham', 'Stornoway']
output = output[~output['Area'].isin(no_sell)]

# In some cases, the ID field does not provide accurate enough conditions to know where the customer is from. Exclude any phone numbers where the join has produced duplicated records.
output = output.drop_duplicates(subset=['Customer Phone Number','Area Code','Area Name','Quantity','Product Code'], keep=False)

# Remove any unwanted fields created from the join. 
output = output[['Customer Phone Number','Area','Quantity','Product Code']]

# Join this dataset to our product lookup table. 
output = pd.merge(output, product_lookup, left_on='Product Code', right_on='Product ID')
output['Value'] = output['Price'].str[1:].astype(float)
output['Quantity'] = output['Quantity'].astype(float)
output['Total'] = output['Value'] * output['Quantity'] 

# For each area, and product, find the total sales values, rounded to zero decimal places 
prod_sales_by_area = output.groupby(['Area','Product Name'])['Total'].sum()
prod_sales_by_area = prod_sales_by_area.to_frame().reset_index()
prod_sales_by_area['Revenue'] = prod_sales_by_area['Total'].round(0).astype(int)

# Rank how well each product sold in each area. 
prod_sales_by_area['Rank'] = prod_sales_by_area.groupby(['Area'])['Revenue'].rank(ascending=False).astype(int)

# For each area, work out the percent of total that each different product contributes to the overall revenue of that Area, rounded to 2 decimal places.
prod_sales_by_area['Area Total'] = prod_sales_by_area['Revenue'].groupby(prod_sales_by_area['Area']).transform('sum')
prod_sales_by_area['% of Total – Product'] = prod_sales_by_area['Revenue'] / prod_sales_by_area['Area Total']
prod_sales_by_area['% of Total – Product'] = prod_sales_by_area['% of Total – Product'].round(2)

# Output the data 
# 5 fields: Rank, Area, Product Name, Revenue, % of Total – Product
output_df = prod_sales_by_area[['Rank', 'Area', 'Product Name', 'Revenue','% of Total – Product']]
output.to_csv('prepped_data\\PD 2021 Wk 9 Output - Product Sales by Area.csv', index=False)

print("data prepped!")
