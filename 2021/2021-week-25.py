# Preppin' Data 2021 Week 25
import pandas as pd
import numpy as np

# Load data
gen_1 = pd.read_excel('unprepped_data\\PD 2021 Wk 25 Input - 2021W25 Input.xlsx', sheet_name='Gen 1')
evolution_group = pd.read_excel('unprepped_data\\PD 2021 Wk 25 Input - 2021W25 Input.xlsx', sheet_name='Evolution Group')
evolutions = pd.read_excel('unprepped_data\\PD 2021 Wk 25 Input - 2021W25 Input.xlsx', sheet_name='Evolutions')
mega_evolutions = pd.read_excel('unprepped_data\\PD 2021 Wk 25 Input - 2021W25 Input.xlsx', sheet_name='Mega Evolutions')
alolan = pd.read_excel('unprepped_data\\PD 2021 Wk 25 Input - 2021W25 Input.xlsx', sheet_name='Alolan')
galarian = pd.read_excel('unprepped_data\\PD 2021 Wk 25 Input - 2021W25 Input.xlsx', sheet_name='Galarian')
gigantamax = pd.read_excel('unprepped_data\\PD 2021 Wk 25 Input - 2021W25 Input.xlsx', sheet_name='Gigantamax')
unattainable = pd.read_excel('unprepped_data\\PD 2021 Wk 25 Input - 2021W25 Input.xlsx', sheet_name='Unattainable in Sword & Shield')
anime = pd.read_excel('unprepped_data\\PD 2021 Wk 25 Input - 2021W25 Input.xlsx', sheet_name='Anime Appearances')

# Clean up the list of Gen 1 Pokémon so we have 1 row per Pokémon
gen_1 = gen_1.loc[gen_1.Name.notnull()]
gen_1['#'] = np.int64(gen_1['#'])

# Clean up the Evolution Group input so that we can join it to the Gen 1 list 
evolution_group['#'] = np.int64(evolution_group['#'])
evol_lookup = evolution_group[['Evolution Group','#']]

evolution_group_df = evolution_group
del evolution_group_df['Evolution Group']
evolution_group_df = evolution_group_df.drop_duplicates()

gen_1_df = pd.merge(gen_1,evolution_group_df, on = '#', how = 'inner')

# Filter out Starter and Legendary Pokémon
gen_1_df = gen_1_df.loc[gen_1_df['Starter?'] == 0]
gen_1_df = gen_1_df.loc[gen_1_df['Legendary?'] == 0]

# Using the Evolutions input, exclude any Pokémon that evolves from a Pokémon that is not part of Gen 1 or can evolve into a Pokémon outside of Gen 1
evolutions_df = evolutions[evolutions['Evolving to'].isin(gen_1_df['Name'])]
evolutions_df = evolutions_df[evolutions_df['Evolving from'].isin(gen_1_df['Name'])]

# create list of evolving to and from
keep = list(evolutions_df['Evolving from'])
keep_2 = list(evolutions_df['Evolving to'])
keep.extend(keep_2)
keep = list(set(keep))

gen_1_df = gen_1_df[gen_1_df['Name'].isin(keep)]

# Exclude any Pokémon with a mega evolution, Alolan, Galarian or Gigantamax form
exclude_df = pd.concat([mega_evolutions,alolan,galarian,gigantamax])
exclude_df['Name'] = exclude_df['Name'].str.replace('^(Mega|Alolan|Galarian|Gigantamax) ','',regex = True)
exclude_df['Name']  = exclude_df['Name'].str.replace(' (X|Y)$','',regex = True)

# find any pokemon that evolves into a mega / gigantamax
id_lookup = gen_1_df[['#','Name']]
exclude_df = pd.merge(exclude_df,id_lookup, on = 'Name', how = 'inner')
exclude_df = pd.merge(exclude_df,evol_lookup, on = '#', how = 'inner')
del exclude_df['#']
exclude_df = pd.merge(exclude_df,evol_lookup, on = 'Evolution Group', how = 'inner')

# exclude pokemon that can mega evolve etc.
gen_1_df = gen_1_df[~gen_1_df['#'].isin(exclude_df['#'])]

# It's not possible to catch certain Pokémon in the most recent games. These are the only ones we will consider from this point on
gen_1_df = gen_1_df[gen_1_df['Name'].isin(list(unattainable['Name']))]

# We're left with 10 evolution groups. Rank them in ascending order of how many times they've appeared in the anime to see who the worst Pokémon is!
# convert anime to evolution groups 
anime_df = pd.merge(anime,id_lookup, left_on = 'Pokemon', right_on = 'Name', how = 'inner')
anime_df = pd.merge(anime_df,evol_lookup, on = '#', how = 'inner')

# count appearances
appearences = anime_df[anime_df['Evolution Group'].isin(list(gen_1_df['Name']))]
appearences = appearences[['Evolution Group','Episode']].drop_duplicates()
appearences = appearences.groupby(['Evolution Group'],as_index=False).count()
appearences.columns = ['Evolution Group','Appearances']

# create rank
appearences['Worst Pokémon'] = appearences['Appearances'].rank(ascending=True)
appearences['Worst Pokémon'] = appearences['Worst Pokémon'].astype(int)

# Output the data
appearences = appearences.sort_values(by='Worst Pokémon', ascending=True).reset_index()
appearences = appearences[['Worst Pokémon','Evolution Group','Appearances']]

appearences.to_csv('prepped_data\\PD 2021 Wk 25 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
