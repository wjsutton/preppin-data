# Preppin' Data 2021 Week 07
import pandas as pd

# Load data
shopping_list = pd.read_excel('unprepped_data\\PD 2021 Wk 7 Input - Shopping List and Ingredients.xlsx', engine='openpyxl', sheet_name = 'Shopping List')
keywords = pd.read_excel('unprepped_data\\PD 2021 Wk 7 Input - Shopping List and Ingredients.xlsx', engine='openpyxl', sheet_name = 'Keywords')

# Prepare the keyword data
#  - Add an 'E' in front of every E number.
#  - Stack Animal Ingredients and E Numbers on top of each other.
#  - Get every ingredient and E number onto separate rows.
animal_ingredients = keywords['Animal Ingredients'][0].split(', ')
e_numbers = keywords['E Numbers'][0].split(', ')
e_numbers = ['E' + x for x in e_numbers]
keyword_list = animal_ingredients + e_numbers
keyword_list = [x.lower() for x in keyword_list]

# Check whether each product contains any non-vegan ingredients.
# Prepare a final shopping list of vegan products.
#  - Aggregate the products into vegan and non-vegan.
#  - Filter out the non-vegan products.

# Prepare a list explaining why the other products aren't vegan.
#  - Keep only non-vegan products.
#  - Duplicate the keyword field.
#  - Rows to columns pivot the keywords using the duplicate as a header.
#  - Write a calculation to concatenate all the keywords into a single comma-separated list for each product, e.g. "whey, milk, egg".

# truncate dataframe to set up non-vegan dfs
non_vegan = shopping_list.truncate(before=-1, after=-1)
reason_list = []

# lowercase ingredients to match keywords
shopping_list['Ingredients/Allergens'] = shopping_list['Ingredients/Allergens'].str.lower()

# loop to see if keyword included in ingredients
for ingredient in keyword_list:
    a = shopping_list[shopping_list['Ingredients/Allergens'].str.contains(ingredient)]
    if len(a) > 0:
        b = [ingredient]
        b = b * len(a)
        reason_list.append(b)
        non_vegan = non_vegan.append(a)

# reduce list of lists to just single list
flat_list = [item for sublist in reason_list for item in sublist]
non_vegan['contains'] = flat_list

# make contains column as concatenated list 
non_vegan['Contains'] = non_vegan[['Product','contains','Description']].groupby(['Product','Description'])['contains'].transform(lambda x: ', '.join(x))
non_vegan = non_vegan[['Product','Description','Contains']].drop_duplicates()

# left join to filter out non-vegan products 
vegan = shopping_list.merge(non_vegan, on='Product', how='left')
vegan = vegan[vegan['Contains'].isnull()]

# reduce dataframe and rename columns
vegan = vegan[['Product','Description_x']]
new_vegan_columns = ['Product','Description']
vegan.columns  = new_vegan_columns

# Output the data.

# writing data to csv
vegan.to_csv('prepped_data\\PD 2021 Wk 7 Output - 1 Vegan List.csv', index=False)
non_vegan.to_csv('prepped_data\\PD 2021 Wk 7 Output - 2 Non-Vegan List.csv', index=False)

print("data prepped!")
