# Preppin' Data 2021 Week 08
# We will need to make some assumptions as part of our data prep:
#  - Customers often don't sing the entire song
#  - Sessions last 60 minutes
#  - Customers arrive a maximum of 10 minutes before their sessions begin

import pandas as pd
import numpy as np
import datetime as dt

# Load data
karaoke_choices = pd.read_excel('unprepped_data\\PD 2021 Wk 8 Input - Karaoke Dataset.xlsx', engine='openpyxl', sheet_name = 'Karaoke Choices')
customers = pd.read_excel('unprepped_data\\PD 2021 Wk 8 Input - Karaoke Dataset.xlsx', engine='openpyxl', sheet_name = 'Customers')

# Calculate the time between songs
karaoke_choices['Next song'] = karaoke_choices['Date'][1:].reset_index(drop=True)
karaoke_choices['Time between songs'] = karaoke_choices['Next song'] - karaoke_choices['Date']

# If the time between songs is greater than (or equal to) 59 minutes, flag this as being a new session
karaoke_choices['Time between songs in minutes'] = karaoke_choices['Time between songs'].dt.total_seconds()/60
karaoke_choices['New session'] = np.where(karaoke_choices['Time between songs in minutes']>=59,1,0)

# Create a session number field
# loop through dataframe and increase session id if new session flagged
session = 1
session_list = []
for i in range(len(karaoke_choices['New session'])):
    session_list.append(session)
    session += karaoke_choices['New session'][i]

karaoke_choices['Session #'] = session_list

# Number the songs in order for each session
karaoke_choices["Song Order"] = karaoke_choices.groupby("Session #")["Date"].rank("dense", ascending=True)
karaoke_choices["Song Order"] = karaoke_choices["Song Order"].astype(int)

# Match the customers to the correct session, based on their entry time

# create session start time column
session_start_df = karaoke_choices[["Session #","Date"]]
session_start_df = session_start_df.loc[session_start_df.groupby("Session #").Date.idxmin()].reset_index(drop=True)

# rename column and merge to dataset
new_session_columns = ['Session #','Session Start']
session_start_df.columns  = new_session_columns
karaoke_choices = karaoke_choices.merge(session_start_df, on='Session #', how='inner')

# create time interval to match datasets on 
threshold = 20
threshold_ns = threshold * 60 * 1e9

# compute "interval" to which each session belongs
karaoke_choices['interval'] = pd.to_datetime(np.round(karaoke_choices['Session Start'].astype(np.int64) / threshold_ns) * threshold_ns)
customers['interval'] = pd.to_datetime(np.round(customers['Entry Time'].astype(np.int64) / threshold_ns) * threshold_ns)

# merge datasets on interval
output = karaoke_choices.merge(customers, on='interval', how='inner')

# Output the data
# 6 fields: Session #, Customer ID, Song Order, Date, Artist, Song
# 988 rows (989 including headers)

# reduce columns for output
output = output[['Session #','Customer ID','Song Order','Date','Artist','Song']]

# writing data to csv
output.to_csv('prepped_data\\PD 2021 Wk 8 Output - Karaoke Output.csv', index=False)

print("data prepped!")
