# Preppin' Data 2022 Week 04
import pandas as pd
import numpy as np
import jellyfish

# Input both data sets
students = pd.read_csv('2022\\unprepped_data\\PD 2022 Wk 1 Input.csv')
travel = pd.read_csv('2022\\unprepped_data\\PD 2022 Wk 4 Input.csv')

# Join the data sets together based on their common field
df = pd.merge(students,travel,how='inner',left_on='id',right_on='Student ID')

# Remove any fields you don't need for the challenge
cols_to_keep = ['Student ID', 'M','Tu', 'W', 'Th','F']
df = df[cols_to_keep]

# Change the weekdays from separate columns to one column of weekdays and one of the pupil's travel choice
df = df.melt(id_vars='Student ID', var_name='Weekday', value_name='Method of Travel Raw')

# Group the travel choices together to remove spelling mistakes
# use jellyfish library to get word soundex and simplify to 2 letters for broad match
df['soundex'] = df['Method of Travel Raw'].apply(lambda x: jellyfish.soundex(x))
df['simple soundex'] = df['soundex'].str[0:2]

travel_map = df[['simple soundex','Method of Travel Raw']]
travel_map = travel_map.groupby(['simple soundex','Method of Travel Raw']).agg(count = ('simple soundex','count')).reset_index()
travel_map['count_max'] = travel_map.groupby(['simple soundex'])['count'].transform(max)

# Reduce to just top match
travel_lookup = travel_map.loc[travel_map['count'] == travel_map['count_max']]

# Manually remove Scoter as equal to max count for correct spelling
travel_lookup = travel_lookup.loc[travel_map['Method of Travel Raw'] != 'Scoter']

travel_lookup = travel_lookup[['simple soundex','Method of Travel Raw']]
travel_lookup = travel_lookup.rename(columns={'Method of Travel Raw':'Method of Travel'})

df = pd.merge(df,travel_lookup,on='simple soundex',how='inner')

# Create a Sustainable (non-motorised) vs Non-Sustainable (motorised) data field 
#  - Scooters are the child type rather than the motorised type
unsustainable = ['Aeroplane','Car','Helicopter','Van']
df['Sustainable?'] = np.where(df['Method of Travel'].isin(unsustainable),'Unsustainable','Sustainable')

# Total up the number of pupil's travelling by each method of travel 
df = df[['Student ID','Weekday','Method of Travel','Sustainable?']]
df = df.groupby(['Weekday','Method of Travel','Sustainable?']).agg(trips=('Student ID','count')).reset_index()

# Work out the % of trips taken by each method of travel each day
df['trips_per_day'] = df.groupby(['Weekday'])['trips'].transform('sum')
df['% of trips per day'] = df['trips']/df['trips_per_day'] 

# Round to 2 decimal places
df['% of trips per day'] = df['% of trips per day'].round(2)

df = df[['Sustainable?','Method of Travel','Weekday','trips','trips_per_day','% of trips per day']]
df = df.rename(columns={'trips':'Number of Trips','trips_per_day':'Trips per day'})

# Writing data to csv
df.to_csv('2022\\python_scripts\\outputs\\PD 2022 Wk 4 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
