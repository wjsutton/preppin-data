# Preppin' Data 2021 Week 36
import pandas as pd
import numpy as np

# Load data
timeline_df = pd.read_excel('unprepped_data\\PD 2021 Wk 36 Input.xlsx', sheet_name='Timeline',skiprows=2)
country_df = pd.read_excel('unprepped_data\\PD 2021 Wk 36 Input.xlsx', sheet_name='Country Breakdown',skiprows=2)

# Calculate the overall average index for each search term
avg_pet_adoption = timeline_df['Pet adoption: (Worldwide)'].mean()
avg_online_streamer = timeline_df['Online streamer: (Worldwide)'].mean()
avg_staycation = timeline_df['Staycation: (Worldwide)'].mean()

# Work out the earliest peak for each of these search terms
peak_pet_adoption = timeline_df.loc[timeline_df['Pet adoption: (Worldwide)'].idxmax()]
peak_online_streamer = timeline_df.loc[timeline_df['Online streamer: (Worldwide)'].idxmax()]
peak_staycation = timeline_df.loc[timeline_df['Staycation: (Worldwide)'].idxmax()]

# reduce to peak week and index value
peak_pet_adoption = [peak_pet_adoption['Pet adoption: (Worldwide)'],peak_pet_adoption['Week']]
peak_online_streamer = [peak_online_streamer['Online streamer: (Worldwide)'],peak_online_streamer['Week']]
peak_staycation = [peak_staycation['Staycation: (Worldwide)'],peak_staycation['Week']]

# For each year (1st September - 31st August), calculate the average index
timeline_df['Report Year'] = (timeline_df['Week'] - pd.Timestamp('2016-09-01 00:00:00'))/np.timedelta64(1, 'Y')
timeline_df['Report Year'] = timeline_df['Report Year'].astype(int) + 2016

yearly_avgs = timeline_df.groupby(['Report Year']).agg(a = ('Pet adoption: (Worldwide)','mean'),b = ('Online streamer: (Worldwide)','mean'),c = ('Staycation: (Worldwide)','mean')).reset_index()
yearly_avgs.columns = ['Report Year','Pet adoption','Online streamer','Staycation']

# Classify each search term as either a Lockdown Fad or Still Trendy based on whether the average index has increased or decreased since last year
rp_2020 = yearly_avgs.loc[yearly_avgs['Report Year']==2020].reset_index()
rp_2019 = yearly_avgs.loc[yearly_avgs['Report Year']==2019].reset_index()
year_on_year_change = rp_2020 - rp_2019

status_pet_adoption = np.where(year_on_year_change['Pet adoption']>=0,'Still Trendy','Lockdown Fad')
status_online_streamer = np.where(year_on_year_change['Online streamer']>=0,'Still Trendy','Lockdown Fad')
status_staycation = np.where(year_on_year_change['Staycation']>=0,'Still Trendy','Lockdown Fad')

# simplify variables to rows for dataframe
pets = ['Pet adoption'] + status_pet_adoption.tolist() + rp_2020['Pet adoption'].tolist() + [avg_pet_adoption.tolist()] + peak_pet_adoption
streamers = ['Online streamer'] + status_online_streamer.tolist() + rp_2020['Online streamer'].tolist() + [avg_online_streamer.tolist()] + peak_online_streamer
stayers = ['Staycation'] + status_staycation.tolist() + rp_2020['Staycation'].tolist() + [avg_staycation.tolist()] + peak_staycation

cols = ['Search Term','Status','2020/21 avg index','Avg index','Index Peak','First Peak']
output_df = pd.DataFrame(np.array([pets,streamers,stayers]),columns=cols)

# Filter the countries so that only those with values for each search term remain
country_df = country_df.dropna(thresh=3)

# For each search term, work out which country has the highest percentage
pet_adoption = country_df.loc[country_df['Pet adoption: (01/09/2016 - 01/09/2021)'].idxmax()]
online_streamer = country_df.loc[country_df['Online streamer: (01/09/2016 - 01/09/2021)'].idxmax()]
staycation = country_df.loc[country_df['Staycation: (01/09/2016 - 01/09/2021)'].idxmax()]

# create data frame rows of [search term, highest country]
pet_adoption = ['Pet adoption',pet_adoption['Country']]
online_streamer = ['Online streamer',online_streamer['Country']]
staycation = ['Staycation',staycation['Country']]

# create dataframe for upcoming join
highest_country_df = pd.DataFrame(np.array([pet_adoption,online_streamer,staycation]),columns=['Search Term','Country with highest percentage'])

# Bring everything together into one dataset
output_df = pd.merge(output_df,highest_country_df,on='Search Term',how='inner')

# Output the data
# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 36 Output.csv', index=False)

print("data prepped!")
