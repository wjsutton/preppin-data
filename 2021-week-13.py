# Preppin' Data 2021 Week 13
import pandas as pd

# Input all the files
pl_15_16 = pd.read_csv('unprepped_data\\PD 2021 Wk 13 Input - pl_15-16.csv')
pl_16_17 = pd.read_csv('unprepped_data\\PD 2021 Wk 13 Input - pl_16-17.csv')
pl_17_18 = pd.read_csv('unprepped_data\\PD 2021 Wk 13 Input - pl_17-18.csv')
pl_18_19 = pd.read_csv('unprepped_data\\PD 2021 Wk 13 Input - pl_18-19.csv')
pl_19_20 = pd.read_csv('unprepped_data\\PD 2021 Wk 13 Input - pl_19-20.csv')

# concat dataframes together
pl_15_20 = pd.concat([pl_15_16,pl_16_17,pl_17_18,pl_18_19,pl_19_20])

# Remove all goalkeepers from the data set
pl_df = pl_15_20.loc[pl_15_20['Position'] != 'Goalkeeper']

# Remove all records where appearances = 0	
pl_df = pl_df.loc[pl_df['Appearances'] != 0]

# In this challenge we are interested in the goals scored from open play
#  - Create a new “Open Play Goals” field (the goals scored from open play is the number of goals scored that weren’t penalties or freekicks)
#  - Note some players will have scored free kicks or penalties with their left or right foot
#  - Be careful how Prep handles null fields! (have a look at those penalty and free kick fields) 
#  - Rename the original Goals scored field to Total Goals Scored

# replace NaNs with 0 throughout
pl_df = pl_df.fillna(0)
pl_df['Open Play Goals'] = pl_df['Goals'] - (pl_df['Penalties scored']+pl_df['Freekicks scored'])
pl_df.rename(columns={'Goals':'Total Goals'}, inplace=True)

# Calculate the totals for each of the key metrics across the whole time period for each player, (be careful not to lose their position)
pl_df_totals = pl_df
# Remove Season column and sum all columns not grouped by
del pl_df_totals['Season']
pl_df_totals = pl_df_totals.groupby(['Name', 'Position']).sum()

# Create an open play goals per appearance field across the whole time period
pl_df_totals['Open Play Goals / Game'] = pl_df_totals['Open Play Goals']/pl_df_totals['Appearances']

# Rank the players for the amount of open play goals scored across the whole time period, we are only interested in the top 20 (including those that are tied for position) – Output 1
pl_df_totals['Rank - Total Open Play Goals'] = pl_df_totals['Open Play Goals'].rank(ascending=False,method='min')
# Reduce to top 20, sort and rename ranking column
output_1 = pl_df_totals.loc[pl_df_totals['Rank - Total Open Play Goals'] <= 20]
output_1 = output_1.sort_values(by='Rank - Total Open Play Goals', ascending=True).reset_index()
output_1['Rank'] = output_1['Rank - Total Open Play Goals']

# Rank the players for the amount of open play goals scored across the whole time period by position, we are only interested in the top 20 (including those that are tied for position) – Output 2
pl_df_totals['Rank - Total Open Play Goals by Position'] = pl_df_totals.groupby('Position')['Open Play Goals'].rank(ascending=False,method='min')
# Reduce to top 20, sort and rename ranking column
output_2 = pl_df_totals.loc[pl_df_totals['Rank - Total Open Play Goals by Position'] <= 20]
output_2 = output_2.sort_values(by='Rank - Total Open Play Goals by Position', ascending=True).reset_index()
output_2['Rank'] = output_2['Rank - Total Open Play Goals by Position']

# Output the data – in your solution on twitter / the forums, state the name of the player who was the only non-forward to make it into the overall top 20 for open play goals scored
print(output_1.loc[output_1['Position'] != 'Forward']['Name'])

# Reduce to just required columns
out1_cols = ['Open Play Goals','Goals with right foot','Goals with left foot','Position','Appearances','Rank','Total Goals','Open Play Goals / Game','Headed goals','Name']
out2_cols = out1_cols

output_1_df = output_1[out1_cols]
output_2_df = output_2[out2_cols]

# Writing data to csv
output_1_df.to_csv('prepped_data\\PD 2021 Wk 13 Output - Overall Rank.csv', index=False)
output_2_df.to_csv('prepped_data\\PD 2021 Wk 13 Output - Rank by Position.csv', index=False)

print("data prepped!")