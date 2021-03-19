# Preppin' Data 2021 Week 11
import pandas as pd
import numpy as np

# Load data
cocktails = pd.read_excel('unprepped_data\\PD 2021 Wk 11 Input - Cocktails Dataset.xlsx', engine='openpyxl', sheet_name = 'Cocktails')
source = pd.read_excel('unprepped_data\\PD 2021 Wk 11 Input - Cocktails Dataset.xlsx', engine='openpyxl', sheet_name = 'Sourcing')
conversion_rates = pd.read_excel('unprepped_data\\PD 2021 Wk 11 Input - Cocktails Dataset.xlsx', engine='openpyxl', sheet_name = 'Conversion Rates')

# Split out the recipes into the different ingredients and their measurements
# Convert ; seperated string to column
ingredients = cocktails['Recipe (ml)'].str.split(';', expand=True).stack()

# Apply to existing data set
indx = ingredients.index._get_level_values(0)
cocktail_df = cocktails.iloc[indx].copy()
cocktail_df['recipe'] = ingredients.values
cocktail_df.drop('Recipe (ml)', axis=1,inplace=True)

# Split ingredient and measurement to own columns
cocktail_df[['Ingredient', 'Measurement']] = cocktail_df['recipe'].str.split(':',expand=True)
cocktail_df['ml'] = cocktail_df['Measurement'].str.extract(r'(\d+)')
cocktail_df['ml'] = cocktail_df['ml'].astype(float)

# Calculate the price in pounds, for the required measurement of each ingredient
source_df = pd.merge(source,conversion_rates,on='Currency',how='inner')
source_df['Price (£)'] = source_df['Price']/source_df['Conversion Rate £']
source_df['price_per_ml'] = source_df['Price (£)']/source_df['ml per Bottle'].astype(float)

# trim whitespace for join
source_df['Ingredient'] = source_df['Ingredient'].str.strip()
cocktail_df['Ingredient'] = cocktail_df['Ingredient'].str.strip()

# Join the ingredient costs to their relative cocktails
costs_df = pd.merge(cocktail_df,source_df[['Ingredient','price_per_ml']],on='Ingredient',how='left')
costs_df['Ingredient cost'] = costs_df['ml']*costs_df['price_per_ml']

# Find the total cost of each cocktail 
cocktail_cost_df = costs_df.groupby(['Cocktail','Price (£)'],as_index=False)['Ingredient cost'].agg('sum')

# Include a calculated field for the profit margin i.e. the difference between each cocktail's price and it's overall cost 
cocktail_cost_df['Profit Margin'] = cocktail_cost_df['Price (£)'] - cocktail_cost_df['Ingredient cost']

# Round all numeric fields to 2 decimal places 
cocktail_cost_df['Profit Margin'] = cocktail_cost_df['Profit Margin'].round(2)
cocktail_cost_df['Ingredient cost'] = cocktail_cost_df['Ingredient cost'].round(2)

# Output
# renaming columns
cocktail_cost_df.columns = ['Cocktail','Price','Cost','Margin']

# writing data to csv
cocktail_cost_df.to_csv('prepped_data\\PD 2021 Wk 11 Output - Cocktail Profit Margin.csv', index=False)

print("data prepped!")