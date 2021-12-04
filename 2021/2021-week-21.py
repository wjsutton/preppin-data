# Preppin' Data 2021 Week 21
import pandas as pd
import numpy as np

# Load data
# Read all Excel tabs and concat as one dateframe
all_tabs = pd.read_excel('unprepped_data\\PD 2021 Wk 21 Input.xlsx', sheet_name=None)

# Bring all the sheets together
all_dfs = []
for tab_name, df in all_tabs.items():
    df['sheet_name'] = tab_name
    all_dfs.append(df)
    trolley_df = pd.concat(all_dfs, ignore_index=True)

# Use the Day of Month and Table Names (sheet name in other tools) to form a date field for the purchase called 'Date'
trolley_df['month'] = trolley_df['sheet_name'].str.replace('Month ', '')
trolley_df['month'] = trolley_df['month'].astype(int)
trolley_df['year'] = '2021'
trolley_df['day'] = trolley_df['Day of Month'].fillna(0.0).astype(int)
trolley_df = trolley_df.loc[trolley_df['day'] > 0]

trolley_df['date'] = pd.to_datetime(trolley_df[['year','month', 'day']])

# Create 'New Trolley Inventory?' field to show whether the purchase was made on or after 1st June 2021 (the first date with the revised inventory after the project closed)
trolley_df['New Trolley Inventory?'] = np.where(trolley_df['date'] >='2021-06-01',True,False)

# Remove lots of the detail of the product name:
# Only return any names before the '-' (hyphen)
# If a product doesn't have a hyphen return the full product name
product_clean = trolley_df['Product'].str.split('-')
product_clean = product_clean.str[0]
trolley_df['Product Clean'] = product_clean
trolley_df['Product Clean'] = trolley_df['Product Clean'].str.strip()

# Make price a numeric field
trolley_df['price_in_dollars'] = trolley_df['Price'].str.replace('$', '',regex=False)
trolley_df['price_in_dollars'] = trolley_df['price_in_dollars'].astype(float)

# Work out the average selling price per product
avg_sell_price = trolley_df.groupby(['Product Clean'],as_index=False)['price_in_dollars'].agg({'Average Sell Price': 'mean'})

# Workout the Variance (difference) between the selling price and the average selling price
trolley_df = pd.merge(trolley_df,avg_sell_price, on ='Product Clean', how='inner')
trolley_df['Price variance'] = trolley_df['price_in_dollars'] - trolley_df['Average Sell Price'] 

# Rank the Variances (1 being the largest positive variance) per destination and whether the product was sold before or after the new trolley inventory project delivery
trolley_df = trolley_df.sort_values(by='Price variance', ascending=False).reset_index()
trolley_df['Destination'] = trolley_df['Destination'].str.strip()
trolley_df['Rank'] = trolley_df.groupby(['Destination','New Trolley Inventory?'])['Price variance'].rank(ascending=False)
trolley_df['Rank'] = trolley_df['Rank'].astype(int)

# Return only ranks 1-5 
output_df = trolley_df.loc[trolley_df['Rank'] <= 5]

# Output the data
output_columns = ['New Trolley Inventory','Variance Rank by Destination','Variance','Average Price per Product','Date','Product','First name','Last Name','Email','Price','Destination']
output_df = output_df[['New Trolley Inventory?','Rank','Price variance','Average Sell Price','date','Product Clean','first_name','last_name','email','Price','Destination']]
output_df.columns = output_columns

output_df.to_csv('prepped_data\\PD 2021 Wk 21 Output.csv', encoding="utf-8-sig", index=False)

# which two products appeared more than once in the rankings and whether they were sold before or after the project delivery. Tweet us your answer!
answer = output_df[output_df.groupby('Product')['Product'].transform('count') > 1]
print(answer[['Product','New Trolley Inventory']])

print("data prepped!")
