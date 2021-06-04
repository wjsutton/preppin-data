# Preppin' Data 2021 Week 22
import pandas as pd
import numpy as np

# Load data
answer_smash = pd.read_excel('unprepped_data\\PD 2021 Wk 22 Answer Smash Input.xlsx', engine='openpyxl', sheet_name = 'Answer Smash')
names = pd.read_excel('unprepped_data\\PD 2021 Wk 22 Answer Smash Input.xlsx', engine='openpyxl', sheet_name = 'Names')
questions = pd.read_excel('unprepped_data\\PD 2021 Wk 22 Answer Smash Input.xlsx', engine='openpyxl', sheet_name = 'Questions')
category = pd.read_excel('unprepped_data\\PD 2021 Wk 22 Answer Smash Input.xlsx', engine='openpyxl', sheet_name = 'Category')

# The category dataset requires some cleaning so that Category and Answer are 2 separate fields
category[['Category', 'Answer']] = category['Category: Answer'].str.split(': ',expand=True)
category['Category'] = category['Category'].str.strip()
category['Answer'] = category['Answer'].str.strip()

# Join the datasets together, making sure to keep an eye on row counts
# Filter the data so that each answer smash is matched with the corresponding name and answer
# Remove unnecessary columns
# Output the data

# Regex joining method: cross-join datasets, check column text matches and then filter away non-matches

# create lower case columns for text match
category['Answer Lower'] = category['Answer'].str.lower()
names['Name Lower'] = names['Name'].str.lower()

answer_smash_df = pd.merge(answer_smash,questions, on = 'Q No', how = 'inner')
answer_smash_df['Answer Smash Lower'] = answer_smash_df['Answer Smash'].str.lower()

# create cross-join column
answer_smash_df['join'] = 1
category['join'] = 1
names['join'] = 1

# Join categories and answer smashes
answer_smash_df = pd.merge(answer_smash_df,category, on = ['Category','join'], how = 'inner')
answer_smash_df['match'] = answer_smash_df.apply(lambda x: x['Answer Smash Lower'].find(x['Answer Lower']), axis=1).ge(0)
answer_smash_df = answer_smash_df.loc[(answer_smash_df['match'] == True)]

# remove columns
del answer_smash_df['Category: Answer']
del answer_smash_df['Answer Lower']
del answer_smash_df['match']

# Join names and answer smashes
answer_smash_df = pd.merge(answer_smash_df,names, on = ['join'], how = 'inner')
answer_smash_df['match'] = answer_smash_df.apply(lambda x: x['Answer Smash Lower'].find(x['Name Lower']), axis=1).ge(0)
answer_smash_df = answer_smash_df.loc[(answer_smash_df['match'] == True)]

# remove columns
del answer_smash_df['join']
del answer_smash_df['Name Lower']
del answer_smash_df['match']

# create output dataset
output_df = answer_smash_df[['Q No','Name','Question','Answer','Answer Smash']]
output_df = output_df.sort_values(by='Q No', ascending=True)

# Writing data to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 22 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
