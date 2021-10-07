# Preppin' Data 2021 Week 40
import pandas as pd
import numpy as np

# Input the data
pet_df = pd.read_csv('unprepped_data\\PD 2021 Wk 40 Input.csv')

# Remove the duplicated date field
del pet_df['MonthYear']

# Filter to only cats and dogs (the other animals have too small a data sample)
pet_df = pet_df.loc[pet_df['Animal Type'].isin(['Cat','Dog'])]

# Group up the Outcome Type field into 2 groups:
#  - Adopted, Returned to Owner or Transferred
#  - Other
pet_df['Outcome Type Group'] = np.where(pet_df['Outcome Type'].isin(['Adoption', 'Return to Owner','Transfer']),'Adopted, Returned to Owner or Transferred','Other')

# Calculate the % of Total for each Outcome Type Grouping and for each Animal Type
# create counts by Animal Type & Outcome Type Group
pet_df = pet_df.groupby(['Animal Type', 'Outcome Type Group']).size().reset_index(name='counts')

# Split into two data frames
art_df = pet_df.loc[pet_df['Outcome Type Group'] == 'Adopted, Returned to Owner or Transferred']
other_df = pet_df.loc[pet_df['Outcome Type Group'] == 'Other']

# reduce columns
art_df = art_df[['Animal Type', 'counts']]
other_df = other_df[['Animal Type', 'counts']]

# rename counts column
art_df.columns = ['Animal Type', 'Adopted, Returned to Owner or Transferred']
other_df.columns = ['Animal Type', 'Other']

# merge two dataframes into one
output_df = pd.merge(art_df,other_df,on='Animal Type',how='inner')

# create total column and calculate percentage for Outcome Type Groups
output_df['Total'] = output_df['Adopted, Returned to Owner or Transferred'] + output_df['Other'] 
output_df['Adopted, Returned to Owner or Transferred'] = output_df['Adopted, Returned to Owner or Transferred']/output_df['Total']
output_df['Other'] = output_df['Other']/output_df['Total']

# Multiple by 100 and round to 1 dp
output_df['Adopted, Returned to Owner or Transferred'] = round(output_df['Adopted, Returned to Owner or Transferred']*100,1)
output_df['Other'] = round(output_df['Other']*100,1)

# Output the data

# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 40 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
