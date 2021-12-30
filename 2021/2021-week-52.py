# Preppin' Data 2021 Week 52
import pandas as pd
import numpy as np

# Load Data
complaints_df = pd.read_excel('unprepped_data\\PD 2021 Wk 52 Input.xlsx', engine='openpyxl', sheet_name = 'Complaints')
dept_res_df = pd.read_excel('unprepped_data\\PD 2021 Wk 52 Input.xlsx', engine='openpyxl', sheet_name = 'Department Responsbile')

# Count the number of complaints per customer
complaints_df['Complaints per Person'] = complaints_df.groupby('Name')['Name'].transform('count')

# Join the 'Department Responsible' data set to allocate the complaints to the correct department
# create matching column and clean up typos
complaints_df['Keyword Search'] = complaints_df['Complaint'].str.lower()
complaints_df['Keyword Search'] = complaints_df['Keyword Search'].str.replace('lugguage','luggage')

# create a regex string of all keywords and extract all matches
pat = "|".join(dept_res_df['Keyword'].str.lower())
all_matches = complaints_df['Keyword Search'].str.extractall("(" + pat + ')').reset_index()

# reduce and rename columns ahead of join
all_matches = all_matches[['level_0',0]]
all_matches.columns = ['index','keyword_match']

# join keyword matches to original complaints (repeats complaint per keyword match)
complaints_df = pd.merge(complaints_df,all_matches,left_on=complaints_df.index,right_on='index',how='left')

# join keywords to department
dept_res_df['keyword_match'] = dept_res_df['Keyword'].str.lower()
df = pd.merge(complaints_df, dept_res_df, how='left', on='keyword_match')

# For any complaint that isn't classified, class the department as 'unknown' and the complaint cause as 'other'
# replace NaNs with fillna
df['keyword_match'] = df['keyword_match'].fillna('other')
df['Department'] = df['Department'].fillna('Unknown')

# Create a comma-separated field for all the keywords found in the complaint for each department
# from: https://stackoverflow.com/questions/27174009/python-pandas-concatenate-rows-with-unique-values
df = df.groupby(['Name', 'Complaint', 'Complaints per Person','Department']).agg(lambda keyword_match: ', '.join(keyword_match)).reset_index()

# Output the data
# reduce, reorder and rename columns ahead of csv writing
output_cols = ['Complaint','Complaints per Person','keyword_match','Department','Name']
df = df[output_cols]
df.rename( columns={'keyword_match':'Complaint causes'}, inplace=True )

# Writing data to csv
df.to_csv('prepped_data\\PD 2021 Wk 52 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
