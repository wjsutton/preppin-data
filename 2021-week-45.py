# Preppin' Data 2021 Week 45
import pandas as pd
import numpy as np
import datetime

# Load data
nov_10 = pd.read_excel('unprepped_data\\PD 2021 Wk 45 Input.xlsx', sheet_name='10th Nov')
nov_11 = pd.read_excel('unprepped_data\\PD 2021 Wk 45 Input.xlsx', sheet_name='11th Nov')
nov_12 = pd.read_excel('unprepped_data\\PD 2021 Wk 45 Input.xlsx', sheet_name='12th Nov')
attendees = pd.read_excel('unprepped_data\\PD 2021 Wk 45 Input.xlsx', sheet_name='Attendees')

# Create a Date field for each Session
nov_10['Date'] = pd.to_datetime('2021-11-10')
nov_11['Date'] = pd.to_datetime('2021-11-11')
nov_12['Date'] = pd.to_datetime('2021-11-12')

session_df = pd.concat([nov_10,nov_11,nov_12])

# Convert Time field to consistent timestamp
session_df['Session Time'] = np.where(session_df['Session Time'].astype('str').str.len()<=2,session_df['Session Time'].astype('str')+':00:00',session_df['Session Time'].astype('str'))
session_df['Session Time'] = np.where(session_df['Session Time'].astype('str').str.len()<=7,'0'+session_df['Session Time'].astype('str'),session_df['Session Time'].astype('str'))

# Bring date and time together as datetime
session_df['Datetime'] = pd.to_datetime(session_df['Date'].astype('str') + ' ' + session_df['Session Time'].astype('str'))

# Create a row for each Attendee and Join on the Lookup Table
session_df['Attendee IDs'] = session_df['Attendee IDs'].str.split(', ')
session_df = session_df.explode('Attendee IDs').reset_index(drop=True)
session_df['Attendee ID'] = session_df['Attendee IDs'].astype('int')

df = pd.merge(session_df,attendees,how='inner',on = 'Attendee ID')

# Create a Direct Contact Field for each Attendee 
#  - These are people they directly meet in the brain dates they attend
# Make sure Attendees don't have their own names listed as Direct Contacts
direct_contacts = df[['Session ID','Attendee ID','Attendee']]
direct_contacts.columns = ['Session ID','Direct ID','Direct Contact']

df = pd.merge(df,direct_contacts,how='inner',on = 'Session ID')
df = df.loc[df['Direct ID'] != df['Attendee ID']]

# Create an Indirect Contact field for each Attendee
#  - These will be the Direct Contacts for each Attendee's Direct Contacts, for sessions that have happened prior to the session where they meet
#  - Remember: order of sessions is important!
# If another attendee is classified as both a Direct and an Indirect Contact, classify them as a Direct Contact
# Reshape the data so that each row represents an attendee and a contact they've made, either Directly or Indirectly, for each subject matter
#  - Ensure there are no duplicates!

# Not 100% sure on the above method, so going a little rogue with a different method to reach the output
# Note to self:
# - Direct Contact: Someone met in a braindate
# - Indirect Contact: Someone you didn't meet in a braindate but you met someone who did

# Reduce dataframe and find first and last time everyone met
direct_df = df[['Subject','Attendee','Direct Contact','Datetime']]
direct_df = direct_df.groupby(['Subject','Attendee','Direct Contact']).agg(first_met = ('Datetime','min'),last_met = ('Datetime','max')).reset_index()

# duplicate dataframe to find who all the direct contacts met (to then find indirects)
indirects = direct_df.copy()
indirects.columns = ['Subject','Direct Contact','Indirect Contact','first_met','last_met']

# Join directs to indirects, remove cases where 
#  - the direct contact hasn't yet met the indirect contact
#  - the indirect contact is the source attendee
indirects = pd.merge(direct_df,indirects,on=['Direct Contact','Subject'],how = 'inner')
indirects = indirects.loc[indirects['last_met_x']>=indirects['first_met_y']]
indirects = indirects.loc[indirects['Attendee']!=indirects['Indirect Contact']]
indirect_df = indirects[['Subject','Attendee','Indirect Contact']]
indirect_df = indirect_df.drop_duplicates()

# Convert direct and indirect contact dataframes into lists to remove all overlaps
direct_ids = direct_df['Subject']+'-'+direct_df['Attendee']+'-'+direct_df['Direct Contact']
direct_ids = direct_ids.drop_duplicates()
direct_ids = direct_ids.to_list()

indirect_ids = indirect_df['Subject']+'-'+indirect_df['Attendee']+'-'+indirect_df['Indirect Contact']
indirect_ids = indirect_ids.drop_duplicates()
indirect_ids = indirect_ids.to_list()

# Remove cases where indirect contacts were met in a braindate (direct contacts)
indirects_final = list(set(indirect_ids) - set(direct_ids))

# Convert lists back into dataframes, and create column for direct/indirect contacts
direct_df = pd.DataFrame()
direct_df['ID'] = direct_ids
direct_df = direct_df['ID'].str.split(pat='-', n=2, expand=True)
direct_df.columns = ['Subject','Attendee','Contact']
direct_df['Contact Type'] = 'Direct Contact'

indirect_df = pd.DataFrame()
indirect_df['ID'] = indirect_ids
indirect_df = indirect_df['ID'].str.split(pat='-', n=2, expand=True)
indirect_df.columns = ['Subject','Attendee','Contact']
indirect_df['Contact Type'] = 'Indirect Contact'

# Stack dataframes and reorder columns for output
output_df = pd.concat([direct_df,indirect_df])
output_df = output_df[['Subject','Attendee','Contact Type','Contact']]

# Output the Data
# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 45 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
