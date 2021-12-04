# Preppin' Data 2021 Week 38
import pandas as pd
import numpy as np

# Load data
trilogy_df = pd.read_excel('unprepped_data\\PD 2021 Wk 38 Input.xlsx', sheet_name='Top 30 Trilogies')
film_df = pd.read_excel('unprepped_data\\PD 2021 Wk 38 Input.xlsx', sheet_name='Films')

# Split out the Number in Series field into Film Order and Total Films in Series
film_df[['Film Order', 'Total Films in Series']] = film_df['Number in Series'].str.split('/',expand=True)

# Work out the average rating for each trilogy
# Work out the highest ranking for each trilogy
trilogy_stats  = film_df.groupby(['Trilogy Grouping'])['Rating'].agg([('Average Rating','mean'),('Highest Rating','max')]).reset_index()

# Rank the trilogies based on the average rating and use the highest ranking metric to break ties (make sure you haven't rounded the numeric fields yet!)
# Note sort by tie break column then rank breaking ties on the first occurrence
trilogy_stats['Trilogy Ranking'] = trilogy_stats.sort_values('Highest Rating', ascending=False)['Average Rating'].rank(method='first', ascending=False)
trilogy_stats['Trilogy Ranking'] = trilogy_stats['Trilogy Ranking'].astype('int')

# Remove the word trilogy from the Trilogy field
trilogy_df['Trilogy'] = trilogy_df['Trilogy'].str.replace('trilogy','')
trilogy_df['Trilogy'] = trilogy_df['Trilogy'].str.strip()

# Bring the 2 datasets together by the ranking fields
output_df = pd.merge(trilogy_df,trilogy_stats,how='inner',on='Trilogy Ranking')
output_df = pd.merge(output_df,film_df,how='inner',on='Trilogy Grouping')

# Output the data
cols = ['Trilogy Ranking','Trilogy','Average Rating','Film Order','Title', 'Rating','Total Films in Series']
output_df = output_df[cols]
output_df = output_df.rename(columns={'Average Rating': 'Trilogy Average'})

# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 38 Output.csv', index=False)

print("data prepped!")
