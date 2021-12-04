# Preppin' Data 2021 Week 41
import pandas as pd
import numpy as np

# Input the data
# delimit based on whitespace otherwise python reads the csv as 1 column of data
south_df = pd.read_csv('unprepped_data\\PD 2021 Wk 41 Input.csv',delim_whitespace=True)

# Rename the penultimate column from P 1 (as it appears in Prep) to Pts
south_df = south_df.rename(columns={'P.1': 'Pts'})

# Exclude null rows
south_df = south_df[south_df.SEASON.notnull()]

# Create a Special Circumstances field with the following categories
#  - Incomplete (for the most recent season)
#  - Abandoned due to WW2 (for the 1939 season)
#  - N/A for full seasons
most_recent_season = max(south_df['SEASON'])
south_df['Special Circumstances'] = np.where(south_df['SEASON']==most_recent_season,'Incomplete',(np.where(south_df['SEASON']=='1939-40','Abandoned due to WW2',None)))

# Ensure the POS field only has values for full seasons
south_df.loc[south_df['Special Circumstances'] == 'Abandoned due to WW2', 'POS'] = None


# Extract the numeric values from the leagues
#  - FL-CH should be assigned a value of 0 
#  - NAT-P should be assigned a value of 5
south_df['league_value'] = south_df['LEAGUE'].str.extract('(\d+)')
south_df.loc[south_df['LEAGUE'] == 'FL-CH', 'league_value'] = 0
south_df.loc[south_df['LEAGUE'] == 'NAT-P', 'league_value'] = 5
south_df['league_value'] = south_df['league_value']

# Create an Outcome field with 3 potential values. (Note: this should apply to all seasons in the data order regardless of any gaps. The current season will have a null value)
#  - Promoted, where they are in a league higher than their current league in the following season
#  - Relegated, where they are in a league lower than their current league in the following season
#  - Same League, where they do not change leagues between seasons
loop = len(south_df['league_value'])
outcome = []
# loop through column 'league_value' comparing current with next value to determine league outcome
for i in range(loop):
    current = i
    next = i+1

    if next == loop:
        entry = None
    
    if next < loop:
        next_l = int(south_df['league_value'][next])
        curr_l = int(south_df['league_value'][current])
        entry = np.where(next_l > curr_l, 'Promoted',np.where(next_l < curr_l, 'Relegated','Same League'))
        entry = entry.tolist()

    outcome = outcome + [entry]

south_df['Outcome'] = outcome

south_df = south_df.rename(columns={'SEASON': 'Season','LEAGUE': 'League'})
cols = ['Season','Outcome','Special Circumstances','League','P','W','D','L','F','A','Pts','POS']
south_df = south_df[cols]

# Create new rows for seasons that were missed due to WW1 and WW2
# Update the fields with relevant values for these new rows
#  - e.g. change their Special Circumstances value to WW1/WW2
missed_seasons = ['1915-16','1916-17','1917-18','1918-19','1940-41','1941-42','1942-43','1943-44','1944-45','1945-46']
missed_special = ['WW1'] * 4 + ['WW2'] * 6
missed = {'Season': missed_seasons, 'Outcome': [None]*10, 'Special Circumstances': missed_special,'League': [None]*10,'P': [None]*10,'W': [None]*10,'D': [None]*10,'L': [None]*10,'F': [None]*10,'A': [None]*10,'Pts': [None]*10,'POS': [None]*10}
missed_df = pd.DataFrame(data=missed)
output_df = pd.concat([south_df,missed_df])

# Output the data
output_df = output_df.sort_values(by=['Season'])

# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 41 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
