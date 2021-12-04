# Preppin' Data 2021 Week 29
import pandas as pd
import numpy as np

# Load data 
events = pd.read_excel('unprepped_data\\PD 2021 Wk 29 Input - Olympic Events.xlsx', sheet_name='Olympics Events')
venues = pd.read_excel('unprepped_data\\PD 2021 Wk 29 Input - Olympic Events.xlsx', sheet_name='Venues')

# Create a correctly formatted DateTime field
events['Date'] = events['Date'].str.replace('_',' ')
events['Date'] = events['Date'].str.replace(r'(\d)(st|nd|rd|th)', r'\1',regex=True)
events['Time'] = events['Time'].str.replace('xx','0:00')

events['Date and time'] = events['Date'].astype(str) + ' ' + events['Time'].astype(str)
events['Datetime'] =  pd.to_datetime(events['Date and time'], format='%d %B %Y %H:%M')

# Parse the event list so each event is on a separate row
# split events
events['Events'] = events['Events'].str.split(', ')

# explode the column
events = events.explode('Events').reset_index(drop=True)

# Group similar sports into a Sport Type field
events['Sport Group'] = events['Sport'].str.lower()
events['Sport Group'] = events['Sport Group'].str.strip()
events['Sport Group'] = events['Sport Group'].str.replace('\.','',regex=True)
events['Sport Group'] = events['Sport Group'].str.replace('^(3x3|artistic|beach|marathon|trampoline|rhythmic) ','',regex=True)
events['Sport Group'] = events['Sport Group'].str.replace('(judo|karate|taekwondo)','martial arts',regex=True)
events['Sport Group'] = events['Sport Group'].str.replace('^cycling .*','cycling',regex=True)
events['Sport Group'] = events['Sport Group'].str.replace('^canoe .*','canoeing',regex=True)
events['Sport Group'] = events['Sport Group'].str.replace('^volley.*','volleyball',regex=True)
events['Sport Group'] = events['Sport Group'].str.replace('^.* ceremony$','ceremony',regex=True)
events['Sport Group'] = events['Sport Group'].str.replace('^.*softball.*$','baseball',regex=True)
events['Sport Group'] = events['Sport Group'].str.replace('^.*tennis.*$','tennis',regex=True)
events['Sport Group'] = events['Sport Group'].str.replace('^gymna.*','gymnastics',regex=True)
events['Sport Group'] = events['Sport Group'].str.strip()
events['Sport Group'] = events['Sport Group'].str.title()

# Combine the Venue table
venues[['Latitude','Longitude']] = venues['Location'].str.split(', ', 1, expand=True)

# Simplify table and create join column
venue_df = venues[['Venue','Latitude','Longitude']].drop_duplicates()
venue_df['Venue'] = venue_df['Venue'].str.title()
events['Venue'] = events['Venue'].str.title()

# join tables
combined_df = pd.merge(events,venue_df,on = 'Venue', how = 'inner')

# Calculate whether the event is a 'Victory Ceremony' or 'Gold Medal' event. 
# (Note, this might not pick up all of the medal events.)
combined_df['Medal Ceremony?'] = combined_df['Events'].str.contains('victory ceremony|gold medal', case=False, regex=True)

# Output the Data
# create columns and reduce data set
combined_df['Events Split'] = combined_df['Events']
combined_df['UK Date Time'] = combined_df['Datetime']
combined_df = combined_df[['Latitude','Longitude','Medal Ceremony?','Sport Group','Events Split','UK Date Time','Date','Sport','Venue']]

# write data to csv
combined_df.to_csv('prepped_data\\PD 2021 Wk 29 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
