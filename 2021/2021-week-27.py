# Preppin' Data 2021 Week 27
import pandas as pd
import numpy as np
from random import randrange
pd.options.mode.chained_assignment = None 

# Load data 
seeding = pd.read_excel('unprepped_data\\PD 2021 Wk 27 Input.xlsx', sheet_name='Seeding')
scaffold = pd.read_excel('unprepped_data\\PD 2021 Wk 27 Input.xlsx', sheet_name='Scaffold')
teams = pd.read_excel('unprepped_data\\PD 2021 Wk 27 Input.xlsx', sheet_name='Teams')

# Create a workflow that will allocate the draft picks 
# in a random manner based on the odds for each team

# The workflow should allocate each of the first 4 picks based 
# on the lottery odds and then allocate all teams that didn't 
# receive a slot to the remaining places in order

# Join seed and teams
df = pd.merge(seeding,teams,on = 'Seed',how='inner')
picks = len(df.columns) - 2

# Set up lists for choice and order
chosen_team = []
pick_order = []

for i in range(picks):
    pick = i + 1
    pick_df = df[['Team',pick]]
    pick_df.columns = ['Team','prob']
    pick_df['pick'] = pick

    # convert probabilities to numeric or null and then filter out nulls
    pick_df['prob'] = pd.to_numeric(pick_df['prob'], errors = 'coerce', downcast = 'float')
    pick_df = pick_df.loc[~pd.isnull(pick_df['prob'])]

    # filter out teams already chosen
    pick_df = pick_df.loc[~pick_df['Team'].isin(chosen_team)].reset_index()

    # convert to out of 1000 and convert to int
    pick_df['prob'] = pick_df['prob']*10
    pick_df['prob'] = pick_df['prob'].astype('int32')

    rows = pick_df['prob'].sum() + 1
    teams_to_pick = len(pick_df)

    # set up list for team probability picking
    a = []

    # loop through dataframe and add teams to list
    for t in range(teams_to_pick):
        a = a + [pick_df['Team'][t]] * pick_df['prob'][t]
    
    # create a dataframe of teams with row numbers to pick from random number generator
    if teams_to_pick > 1:
        row_id = list(range(1, rows))
        decision_df = pd.DataFrame()
        decision_df['row_id'] = row_id
        decision_df['Team'] = a
        chosen = randrange(1,rows)
        choice = decision_df.loc[decision_df['row_id'] == chosen]['Team'].astype(str).values[0]

    # if only 1 team left, pick that team
    if teams_to_pick == 1:
        choice = pick_df['Team'][0]
    
    # Assign choices and order to lists 
    chosen_team = chosen_team + [choice]
    pick_order = pick_order + [pick]

# setup dataframe of choices
output_df = pd.DataFrame()
output_df['Team'] = chosen_team
output_df['Actual Pick'] = pick_order

# join to original seed for output, reorder and rename cols
output_df = pd.merge(output_df,df[['Seed','Team']], on ='Team', how = 'inner')
output_df = output_df[['Actual Pick','Seed','Team']]
output_df.columns = ['Actual Pick','Original','Team']

# write data to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 27 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
