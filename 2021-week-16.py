# Preppin' Data 2021 Week 16
import pandas as pd
import numpy as np

# remove warnings
pd.set_option('mode.chained_assignment', None)

# Input the files
fixtures = pd.read_csv('unprepped_data\\PD 2021 Wk 16 Input - PL Fixtures.csv')

# Filter out matches which haven't been played yet
played_matches = fixtures[fixtures['Result'].notnull()]

# Split out goals from result field
played_matches[['Home Team Goals','Away Team Goals']] = played_matches['Result'].str.split(' - ', expand=True)
played_matches[['Home Team Goals','Away Team Goals']] = played_matches[['Home Team Goals','Away Team Goals']].astype(int)

# Assign points from match result for home and away teams:
# - Win - 3 Points
#  - Draw - 1 Point
#  - Lose - 0 Points
played_matches['Home Team Points'] = np.select(
    [
        played_matches['Home Team Goals'] == played_matches['Away Team Goals'], 
        played_matches['Home Team Goals'] > played_matches['Away Team Goals'],
        played_matches['Home Team Goals'] < played_matches['Away Team Goals']
    ], 
    [
        1, 
        3,
        0
    ], 
    default='Unknown'
)

played_matches['Away Team Points'] = np.select(
    [
        played_matches['Away Team Goals'] == played_matches['Home Team Goals'], 
        played_matches['Away Team Goals'] > played_matches['Home Team Goals'],
        played_matches['Away Team Goals'] < played_matches['Home Team Goals']
    ], 
    [
        1, 
        3,
        0
    ], 
    default='Unknown'
)

# calculate goal difference for home and away teams 
played_matches['Home Team Goals Difference'] = played_matches['Home Team Goals'] - played_matches['Away Team Goals']
played_matches['Away Team Goals Difference'] = played_matches['Away Team Goals'] - played_matches['Home Team Goals'] 

# split home and away teams into seperate data frames to stack later
home_teams = played_matches[['Round Number','Date','Location','Home Team','Home Team Goals','Home Team Points','Home Team Goals Difference']]
away_teams = played_matches[['Round Number','Date','Location','Away Team','Away Team Goals','Away Team Points','Away Team Goals Difference']]

columns = ['Round Number','Date','Location','Team','Team Goals','Team Points','Team Goals Difference']

home_teams.columns = columns
away_teams.columns = columns

# stack home and away data frames
teams_df = pd.concat([home_teams,away_teams])

# convert points to int form str
teams_df['Team Points'] = teams_df['Team Points'].astype(int)

# create 3 data frames for the aggregations and then merge together
points = teams_df.groupby(['Team'],as_index=False)['Team Points'].agg({'Total Points': 'sum'})
diff = teams_df.groupby(['Team'],as_index=False)['Team Goals Difference'].agg({'Goal Difference': 'sum'})
matches = teams_df.groupby(['Team'],as_index=False)['Team Points'].agg({'Total Games Played': 'count'})

output_1 = pd.merge(points,diff, on='Team', how = 'inner')
output_1 = pd.merge(output_1,matches, on='Team', how = 'inner')

# Determine team positons by points then goal difference
output_1 = output_1.sort_values(by=['Total Points','Goal Difference'], ascending=[False,False]).reset_index()
output_1 = output_1.reset_index(drop=True)
output_1['Position'] = output_1.index +1

# Clean up data frame for output
del output_1['index'] 
output_1 = output_1[['Position','Team','Total Points','Goal Difference','Total Games Played']]

# Writing data to csv
output_1.to_csv('prepped_data\\PD 2021 Wk 16 Output - Current League Table.csv', index=False)

# Assuming that the 'Big 6' didn't play any games this season, recalculate the league table.
# After removing the 6 clubs, how has the position changed for the remaining clubs?
big_six = ['Man City','Man Utd','Arsenal','Chelsea','Liverpool','Spurs']

# Rerun earlier process filtering out the big six
played_matches_new = played_matches.loc[~played_matches['Home Team'].isin(big_six)]
played_matches_new = played_matches_new.loc[~played_matches_new['Away Team'].isin(big_six)]

# split home and away teams into seperate data frames to stack later
home_teams = played_matches_new[['Round Number','Date','Location','Home Team','Home Team Goals','Home Team Points','Home Team Goals Difference']]
away_teams = played_matches_new[['Round Number','Date','Location','Away Team','Away Team Goals','Away Team Points','Away Team Goals Difference']]

columns = ['Round Number','Date','Location','Team','Team Goals','Team Points','Team Goals Difference']

home_teams.columns = columns
away_teams.columns = columns

# stack home and away data frames
new_league_df = pd.concat([home_teams,away_teams])
new_league_df['Team Points'] = new_league_df['Team Points'].astype(int)

# create 3 data frames for the aggregations and then merge together
points = new_league_df.groupby(['Team'],as_index=False)['Team Points'].agg({'Total Points': 'sum'})
diff = new_league_df.groupby(['Team'],as_index=False)['Team Goals Difference'].agg({'Goal Difference': 'sum'})
matches = new_league_df.groupby(['Team'],as_index=False)['Team Points'].agg({'Total Games Played': 'count'})

output_2 = pd.merge(points,diff, on='Team', how = 'inner')
output_2 = pd.merge(output_2,matches, on='Team', how = 'inner')

# Determine team positons by points then goal difference
output_2 = output_2.sort_values(by=['Total Points','Goal Difference'], ascending=[False,False]).reset_index()
output_2 = output_2.reset_index(drop=True)
output_2['Position'] = output_2.index +1

# Clean up data frame for output
del output_2['index'] 
output_2 = output_2[['Position','Team','Total Points','Goal Difference','Total Games Played']]

# Add previous rank to calculate change in position
previous_rank = output_1[['Position','Team']]
previous_rank.columns = ['Previous Position','Team']

output_2 = pd.merge(output_2,previous_rank, on='Team', how = 'inner')
output_2['Position Change'] = output_2['Previous Position'] - output_2['Position']
output_2 = output_2[['Position Change','Position','Team','Total Points','Goal Difference','Total Games Played']]

# Writing data to csv
output_2.to_csv('prepped_data\\PD 2021 Wk 16 Output - New League Table.csv', index=False)

print("data prepped!")

