# Preppin' Data 2021 Week 10
import pandas as pd
import numpy as np

# Load data
pkmn = pd.read_excel('unprepped_data\\PD 2021 Wk 10 Input - Pokemon Input.xlsx', engine='openpyxl', sheet_name = 'Pokemon')
evolve = pd.read_excel('unprepped_data\\PD 2021 Wk 10 Input - Pokemon Input.xlsx', engine='openpyxl', sheet_name = 'Evolution')

# Our Pokémon dataset actually contains too many Pokémon:
#  - We're only interested in Pokémon up to Generation III, which is up to (and including) number 386
#  - This means we're also not interested in mega evolutions so we can filter Pokémon whose name start with "Mega"
pkmn['id'] = pkmn['#']
pkmn_df = pkmn.astype({'id': 'float'})
pkmn_df = pkmn_df.loc[pkmn_df['id'] <= 386]

pkmn_df['name_lower'] = pkmn_df['Name'].str.lower()
pkmn_df = pkmn_df[~pkmn_df['name_lower'].str.contains(r'mega ')]

# Some Pokémon have more than one Type. We aren't interested in Types for this challenge so remove this field and ensure we have one row per Pokémon 
pkmn_df = pkmn_df.drop('Type', 1)
pkmn_df = pkmn_df.drop_duplicates()

# Now we want to bring in information about what our Pokémon evolve to 
# Warning!  In our Evolution dataset, we still have Pokémon beyond Gen III. You'll need to filter these out too, from both the evolved from and evolved to fields 
gen_3 = pkmn_df['Name']
evolve_df = evolve[evolve['Evolving from'].isin(gen_3)]
evolve_df = evolve_df[evolve_df['Evolving to'].isin(gen_3)]

# Bring in information about what a Pokémon evolves from 
# Ensure that we have all 386 of our Pokémon, with nulls if they don't have a pre-evolved form or if they don't evolve
pkmn_df = pd.merge(pkmn_df, evolve_df[['Evolving from','Evolving to']], left_on='Name', right_on='Evolving to', how='left')
pkmn_df = pd.merge(pkmn_df, evolve_df, left_on='Name', right_on='Evolving from', how='left')
pkmn_df = pkmn_df.drop(['Evolving to_x', 'Evolving from_y'], 1)
pkmn_df = pkmn_df.drop_duplicates()

# Finally, for Pokémon that have 3 evolutions, we want to know what the First Evolution is in their Evolution Group 
# Some duplication may have occurred with all our joins, ensure no 2 rows are exactly the same 
# Create a calculation for our Evolution Group 

# find all triple evolvers
triple_evolvers = pkmn_df[['Name','Evolving from_x','Evolving to_y']]
triple_evolvers = triple_evolvers[triple_evolvers['Evolving from_x'].notnull()]
triple_evolvers = triple_evolvers[triple_evolvers['Evolving to_y'].notnull()]
triple_evolvers['Evolution Group'] = triple_evolvers['Evolving from_x']

a = triple_evolvers[['Name','Evolution Group']]
b = triple_evolvers[['Evolving from_x','Evolution Group']]
c = triple_evolvers[['Evolving to_y','Evolution Group']]
b.columns = ['Name','Evolution Group']
c.columns = ['Name','Evolution Group']

# append data frames together to make each triple evolving pkmn map to an evolution group
evolve_group_df = triple_evolvers[['Name','Evolution Group']]
evolve_group_df = evolve_group_df.append(b)
evolve_group_df = evolve_group_df.append(c)
evolve_group_df = evolve_group_df.drop_duplicates()

# find double & non-evolvers
double_evolvers = pkmn_df[['Name','Evolving from_x']]
double_evolvers = double_evolvers[~double_evolvers['Name'].isin(evolve_group_df['Name'])]
double_evolvers = double_evolvers[~double_evolvers['Evolving from_x'].isin(evolve_group_df['Name'])]
double_evolvers['Evolution Group'] = np.where(double_evolvers['Evolving from_x'].notnull(), double_evolvers['Evolving from_x'], double_evolvers['Name'])
double_evolvers = double_evolvers[['Name','Evolution Group']]

# append double & non-evolvers with triple evolvers
evolve_group_df = evolve_group_df.append(double_evolvers)
evolve_group_df = evolve_group_df.drop_duplicates()

# The Evolution Group will be named after the First Evolution e.g. in the above example, Bulbasaur is the name of the Evolution Group
pkmn_df = pd.merge(pkmn_df, evolve_group_df, on='Name', how='left')

# Output
output = pkmn_df[['Evolution Group','#','Name','Total','HP','Attack','Defense','Special Attack','Special Defense','Speed','Evolving from_x','Evolving to_y','Level', 'Condition','Evolution Type']]
output.columns = ['Evolution Group','#','Name','Total','HP','Attack','Defense','Special Attack','Special Defense','Speed','Evolving from','Evolving to','Level', 'Condition','Evolution Type']
output = output.drop_duplicates()

# writing data to csv
output.to_csv('prepped_data\\PD 2021 Wk 10 Output - Pokemon.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
