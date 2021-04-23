# Preppin' Data 2021 Week 16
import pandas as pd
import numpy as np

# Load data

# Input the files
fixtures = pd.read_csv('unprepped_data\\PD 2021 Wk 16 Input - PL Fixtures.csv')
print(fixtures)

# Calculate the Total Points for each team. The points are as follows: 
#  - Win - 3 Points
#  - Draw - 1 Point
#  - Lose - 0 Points

#played_matches = fixtures.drop(fixtures[fixtures.isnull()].index, inplace=True)

#print(played_matches)
played_matches = fixtures[fixtures['Result'].notnull()]
#played_matches = fixtures.loc[~(fixtures.Result.isnull())]

# split out goals
played_matches[['Home Team Goals','Away Team Goals']] = played_matches['Result'].str.split(' - ', expand=True)

played_matches[['Home Team Goals','Away Team Goals']] = played_matches[['Home Team Goals','Away Team Goals']].astype(int)

played_matches['Home Team Result'] = np.select(
    [
        played_matches['Home Team Goals'] == played_matches['Away Team Goals'], 
        played_matches['Home Team Goals'] > played_matches['Away Team Goals'],
        played_matches['Home Team Goals'] < played_matches['Away Team Goals']
    ], 
    [
        'Draw', 
        'Win',
        'Lose'
    ], 
    default='Unknown'
)

played_matches['Away Team Result'] = np.select(
    [
        played_matches['Away Team Goals'] == played_matches['Home Team Goals'], 
        played_matches['Away Team Goals'] > played_matches['Home Team Goals'],
        played_matches['Away Team Goals'] < played_matches['Home Team Goals']
    ], 
    [
        'Draw', 
        'Win',
        'Lose'
    ], 
    default='Unknown'
)

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

played_matches['Home Team Goals Difference'] = played_matches['Home Team Goals'] - played_matches['Away Team Goals']
played_matches['Away Team Goals Difference'] = played_matches['Away Team Goals'] - played_matches['Home Team Goals'] 

home_teams = played_matches[['Round Number','Date','Location','Home Team','Home Team Goals','Home Team Result','Home Team Points','Home Team Goals Difference']]
away_teams = played_matches[['Round Number','Date','Location','Away Team','Away Team Goals','Away Team Result','Away Team Points','Away Team Goals Difference']]

columns = ['Round Number','Date','Location','Team','Team Goals','Team Result','Team Points','Team Goals Difference']

home_teams.columns = columns
away_teams.columns = columns

teams_df = pd.concat([home_teams,away_teams])

teams_df['Team Points'] = teams_df['Team Points'].astype(int)

print(teams_df)
points = teams_df.groupby(['Team'],as_index=False)['Team Points'].agg({'Total Points': 'sum'})
diff = teams_df.groupby(['Team'],as_index=False)['Team Goals Difference'].agg({'Goal Difference': 'sum'})
matches = teams_df.groupby(['Team'],as_index=False)['Team Points'].agg({'Total Games Played': 'count'})

output_1 = pd.merge(points,diff, on='Team', how = 'inner')
output_1 = pd.merge(output_1,matches, on='Team', how = 'inner')

#output_1['Rank'] = output_1['Total Points'].rank(method="dense", ascending=False)
#output_1['Rank'] = output_1['Rank'].astype(int) 

#.reset_index(drop=True)
output_1 = output_1.sort_values(by=['Total Points','Goal Difference'], ascending=[False,False]).reset_index()
output_1 = output_1.reset_index(drop=True)
output_1['Rank'] = output_1.index +1
del output_1['index'] 
output_1 = output_1[['Rank','Team','Total Points','Goal Difference','Total Games Played']]

#col1 = output_1['Total Points'].astype(str) 
#col2 = output_1["TotalRevenue"].astype(str)
#df['Rank'] = (col1+col2).astype(int).rank(method='dense', ascending=False).astype(int)

#output_1['Rank'] = output_1.groupby('Team')['Total Points','Goal Difference'].rank(ascending=[False,False])
#output_1['Rank'] = output_1['Rank'].astype(int)

#output_1['Rank'] = output_1(['Area'])['Revenue'].rank(ascending=False).astype(int)
print(output_1)
# games played
# total points
# goal difference


# Calculate the goal difference for each team. Goal difference is the difference between goals scored and goals conceded. 
# Calculate the current rank/position of each team. This is based on Total Points (high to low) and in a case of a tie then Goal Difference (high to low).
# The current league table is our first output.

# Assuming that the 'Big 6' didn't play any games this season, recalculate the league table.
# After removing the 6 clubs, how has the position changed for the remaining clubs?
# The updated league table is the second output.