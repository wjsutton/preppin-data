# Preppin' Data 2021 Week 34
import pandas as pd
import numpy as np
import jellyfish

# Load data
sales_df = pd.read_excel('unprepped_data\\PD 2021 Wk 34 Input.xlsx', sheet_name='Employee Sales')
targets_df = pd.read_excel('unprepped_data\\PD 2021 Wk 34 Input.xlsx', sheet_name='Employee Targets')

# Calculate the Average Monthly Sales for each employee
# Average all columns but first 2
sales_df['Monthly Average'] = sales_df[sales_df.columns.difference(['Store','Employee'])].mean(axis=1)

# In the Targets sheet the Store Name needs cleaning up
# one str.replace as Vim not mapping to Wim in soundex
targets_df['Store'] = targets_df['Store'].str.replace('Vim','Wim')

# use jellyfish library to get word soundex and simplify to 2 letters for broad match
targets_df['soundex'] = targets_df['Store'].apply(lambda x: jellyfish.soundex(x))
targets_df['simple soundex'] = targets_df['soundex'].str[0:2]

store_mapping = targets_df[['simple soundex','Store']]
store_mapping = store_mapping.groupby(['simple soundex','Store']).agg(count = ('simple soundex','count')).reset_index()
store_mapping['count_max'] = store_mapping.groupby(['simple soundex'])['count'].transform(max)

# Reduce to just top match
store_lookup = store_mapping.loc[store_mapping['count'] == store_mapping['count_max']]
store_lookup = store_lookup[['simple soundex','Store']]
store_lookup = store_lookup.rename(columns={'Store':'Store Clean'})

store_lookup = pd.merge(store_mapping,store_lookup,on='simple soundex',how='inner')
store_lookup = store_lookup[['Store','Store Clean']].drop_duplicates()

# Apply to targets_df
targets_df = pd.merge(targets_df,store_lookup,on='Store',how='inner')

# Clean up targets_df
targets_df = targets_df[['Store Clean','Employee','Monthly Target']]
targets_df = targets_df.rename(columns={'Store Clean':'Store'})

# Filter the data so that only employees who are below 90% of their target on average remain
sales_df = pd.merge(sales_df,targets_df,on=['Store','Employee'],how='inner')
sales_df['Target %'] = sales_df['Monthly Average'] / sales_df['Monthly Target']
sales_df = sales_df.loc[sales_df['Target %'] < 0.9]

# For these employees, we also want to know the % of months that they met/exceeded their target
output_df = pd.melt(sales_df, id_vars=['Store','Employee','Monthly Average','Monthly Target','Target %'], var_name='Month', value_name='Sales')
output_df['Above Target'] = np.where(output_df['Sales'] > output_df['Monthly Target'],1,0)
output_df['Months'] = 1
output_df = output_df.groupby(['Store','Employee','Monthly Average','Monthly Target','Target %']).agg(above_target = ('Above Target','sum'),months = ('Months','sum')).reset_index()
output_df['% months target met'] = output_df['above_target'] / output_df['months']

# Output the data
# Format and rename columns
output_df['% months target met'] = round(output_df['% months target met']*100,0)
output_df['Monthly Average'] = round(output_df['Monthly Average'],0)
output_df = output_df.rename(columns={'Monthly Average':'Avg monthly Sales'})

# reorder columns 
cols = ['Store','Employee','Avg monthly Sales','% months target met','Monthly Target']
output_df = output_df[cols]

# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 34 Output.csv', index=False)

print("data prepped!")
