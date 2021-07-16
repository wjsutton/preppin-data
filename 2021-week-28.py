# Preppin' Data 2021 Week 28
import pandas as pd
import numpy as np
import re

# Load data 
world_cup = pd.read_excel('unprepped_data\\PD 2021 Wk 28 Input - InternationalPenalties.xlsx', sheet_name='WorldCup')
euros = pd.read_excel('unprepped_data\\PD 2021 Wk 28 Input - InternationalPenalties.xlsx', sheet_name='Euros')

# Determine what competition each penalty was taken in
world_cup['Event'] = 'World Cup ' + world_cup['Round'] + ' ' + world_cup['Event Year'].astype(str)
euros['Event'] = 'Euros ' + euros['Round'] + ' ' + euros['Event Year'].astype(str)

# trim whitespace
world_cup.columns = world_cup.columns.str.strip()
euros.columns = euros.columns.str.strip()

# lowercase columns
world_cup.columns = world_cup.columns.str.lower()
euros.columns = euros.columns.str.lower()

# stack data frames
penalty_df = pd.concat([world_cup,euros])

# Clean any fields, correctly format the date the penalty was taken, & group the two German countries (eg, West Germany & Germany)
penalty_df['event year'] = penalty_df['event year'].str.replace(',', '', regex=True)
penalty_df['event'] = penalty_df['event'].str.replace(',', '', regex=True)
penalty_df['date'] = pd.to_datetime(penalty_df['date'])

penalty_df['winner'] = penalty_df['winner'].str.strip()
penalty_df['loser'] = penalty_df['loser'].str.strip()

penalty_df['winner'] = penalty_df['winner'].str.replace('^(West|East) ', '', regex=True)
penalty_df['loser'] = penalty_df['loser'].str.replace('^(West|East) ', '', regex=True)

# Rank the countries on the following: 
# - Shootout win % (exclude teams who have never won a shootout)
# - Penalties scored %
# What is the most and least successful time to take a penalty? (What penalty number are you most likely to score or miss?)

# determine which penalties were scored, missed or not taken (result already determined)
penalty_df['winning team scored'] = penalty_df['winning team taker'].str.contains(' scored')
penalty_df['losing team scored'] = penalty_df['losing team taker'].str.contains(' scored')

penalty_df['winning team penalty score'] = np.where(penalty_df['winning team scored'] == True, 1, np.where(penalty_df['winning team scored'] == False,0,None))
penalty_df['losing team penalty score'] = np.where(penalty_df['losing team scored'] == True, 1, np.where(penalty_df['losing team scored'] == False,0,None))

# create data frame of shootout results
penalty_winners = penalty_df[['event','winner']]
penalty_losers = penalty_df[['event','loser']]

penalty_winners = penalty_winners.drop_duplicates()
penalty_losers = penalty_losers.drop_duplicates()

penalty_winners.columns = ['event','team']
penalty_losers.columns = ['event','team']

penalty_winners['result'] = 1
penalty_losers['result'] = 0

shootout_df = pd.concat([penalty_winners,penalty_losers])
shootout_df['played'] = 1

# from shootout_df calculate Shootout win % (exclude teams who have never won a shootout)
# total shoot out results by team, filter non-winners
percent_shootout = shootout_df.groupby(['team']).agg({'result':'sum','played':'sum'}).reset_index()
percent_shootout = percent_shootout.loc[percent_shootout['result'] > 0]

# calculate columns for output
percent_shootout['Shootout Win %'] = percent_shootout['result'] / percent_shootout['played']
percent_shootout['Total Shootouts'] = percent_shootout['played']
percent_shootout['Shootouts'] = percent_shootout['result']
percent_shootout['Team'] = percent_shootout['team']

# calculate rank, sort data frame, reduce and reorder columns
percent_shootout['Win % Rank'] = percent_shootout['Shootout Win %'].rank(method='dense',ascending=False).astype(int)
percent_shootout = percent_shootout.sort_values(by='Win % Rank', ascending=True).reset_index()
percent_shootout = percent_shootout[['Win % Rank','Shootout Win %','Total Shootouts','Shootouts','Team']]

# create data frame of penalties
penalty_win_details = penalty_df[['event','winner','penalty number','winning team penalty score']]
penalty_lose_details = penalty_df[['event','loser','penalty number','losing team penalty score']]

penalty_win_details.columns = ['event','team','penalty number','penalty score']
penalty_lose_details.columns = ['event','team','penalty number','penalty score']

penalty_details = pd.concat([penalty_win_details,penalty_lose_details])
penalty_details = penalty_details.loc[~penalty_details['penalty score'].isnull()]
penalty_details['count'] = 1

# from penalty_details calcuate Penalties scored %
# total penalties of taken and scored by team
penalty_success = penalty_details.groupby(['team']).agg({'penalty score':'sum','count':'sum'}).reset_index()

# calculate columns for output
penalty_success['% Total Penalties Scored'] = penalty_success['penalty score'] / penalty_success['count']
penalty_success['Penalties Missed'] = penalty_success['count'] - penalty_success['penalty score']
penalty_success['Penalties Scored'] = penalty_success['penalty score']
penalty_success['Team'] = penalty_success['team']

# calculate rank, sort data frame, reduce and reorder columns
penalty_success['Penalties Scored %Rank'] = penalty_success['% Total Penalties Scored'].rank(method='dense',ascending=False).astype(int)
penalty_success = penalty_success.sort_values(by='Penalties Scored %Rank', ascending=True).reset_index()
penalty_success = penalty_success[['Penalties Scored %Rank','% Total Penalties Scored','Penalties Missed','Penalties Scored','Team']]

# from penalty_details calcuate What is the most and least successful time to take a penalty?
# total penalties of taken and scored by team
penalty_num_df = penalty_details.groupby(['penalty number']).agg({'penalty score':'sum','count':'sum'}).reset_index()

# calculate columns for output
penalty_num_df['Penalty Scored %'] = penalty_num_df['penalty score'] / penalty_num_df['count']
penalty_num_df['Penalties Scored'] = penalty_num_df['penalty score']
penalty_num_df['Penalties Missed'] = penalty_num_df['count'] - penalty_num_df['penalty score']
penalty_num_df['Total Penalties'] = penalty_num_df['count']
penalty_num_df['Penalty Number'] = penalty_num_df['penalty number']

# calculate rank, sort data frame, reduce and reorder columns
penalty_num_df['Rank'] = penalty_num_df['Penalty Scored %'].rank(method='dense',ascending=False).astype(int)
penalty_num_df = penalty_num_df.sort_values(by='Rank', ascending=True).reset_index()
penalty_num_df = penalty_num_df[['Rank','Penalty Scored %','Penalties Scored','Penalties Missed','Total Penalties','Penalty Number']]

# Output the Data
# write data to Excel file
with pd.ExcelWriter('prepped_data\\PD 2021 Wk 28 Output.xlsx') as writer:  
    percent_shootout.to_excel(writer, sheet_name='Win %', index=False)
    penalty_num_df.to_excel(writer, sheet_name='Penalty Position', index=False)
    penalty_success.to_excel(writer, sheet_name='Score %', index=False)

print("data prepped!")
