# Preppin' Data 2021 Week 47
import pandas as pd
import numpy as np

# Load data
players = pd.read_excel('unprepped_data\\PD 2021 Wk 47 Input.xlsx', sheet_name='top_100')
events = pd.read_excel('unprepped_data\\PD 2021 Wk 47 Input.xlsx', sheet_name='top_100_poker_events')

# Add the player names to their poker events
player_name_lookup = players[['player_id','name']]
event_df = pd.merge(events, player_name_lookup, on = 'player_id', how='inner')

# Create a column to count when the player finished 1st in an event
event_df['won_event'] = np.where(event_df['player_place']=='1st',1,0)

# Replace any nulls in prize_usd with zero
event_df['prize_usd'].fillna(0, inplace=True)

# Find the dates of the players first and last events
event_range = event_df.groupby(['player_id']).agg(first_event = ('event_date','min'),last_event = ('event_date','max')).reset_index()

# Use these dates to calculate the length of poker career in years (with decimals)
event_range['career_length'] = (event_range['last_event'] - event_range['first_event']).dt.days / 365.25

# Create an aggregated view to find the following player stats:
# - Number of events they've taken part in
# - Total prize money
# - Their biggest win
# - The percentage of events they've won
# - The distinct count of the country played in
# - Their length of career
player_stats = event_df.groupby(['player_id','name']).agg(number_of_events = ('event_date','count'),total_prize_money = ('prize_usd','sum'),biggest_win = ('prize_usd','max'),events_won=('won_event','sum'),countries_visited=('event_country','nunique')).reset_index()
player_stats['percentage_won'] = player_stats['events_won'] / player_stats['number_of_events']
player_stats = pd.merge(player_stats,event_range[['player_id','career_length']],on='player_id',how='inner')

# Reduce the data to name, number of events, total prize money, biggest win, 
# percentage won, countries visited, career length
del player_stats['player_id']
del player_stats['events_won']

# Creating a Pizza Plot / Coxcomb chart output:
# Using the player stats to create two pivot tables
#  - a pivot of the raw values
#  - a pivot of the values ranked from 1-100, with 100 representing the highest value
# Note: we're using a ranking method that averages ties, pay particular attention to countries visited!
# Join the pivots together
player_pivot = pd.melt(player_stats, id_vars=['name'], var_name='metric',value_name='raw_value')

# create average rank from max + min / 2
player_pivot["rank_max"] = player_pivot.groupby("metric")["raw_value"].rank("max", ascending=True)
player_pivot["rank_min"] = player_pivot.groupby("metric")["raw_value"].rank("min", ascending=True)
player_pivot["rank_avg"] = (player_pivot["rank_min"] + player_pivot["rank_max"]) / 2

# Output the data
del player_pivot['rank_max']
del player_pivot['rank_min']
player_pivot = player_pivot.rename(columns={'rank_avg':'scaled_value'})

# Write to csv
player_pivot.to_csv('prepped_data\\PD 2021 Wk 47 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
