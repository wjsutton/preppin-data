# Preppin' Data 2021 Week 32
import pandas as pd
import numpy as np
import datetime as dt

# Load data
ticket_df = pd.read_csv('unprepped_data\\PD 2021 Wk 32 Input.csv')

# Form Flight name
ticket_df['Flight'] = ticket_df['Departure'] +' to '+ ticket_df['Destination']

# Workout how many days between the sale and the flight departing
ticket_df['Date of Flight'] = pd.to_datetime(ticket_df['Date of Flight'],format = "%d/%m/%Y")
ticket_df['Date'] = pd.to_datetime(ticket_df['Date'],format = "%d/%m/%Y")
ticket_df['Days until flight'] = (ticket_df['Date of Flight'] - ticket_df['Date']).dt.days

# Classify daily sales of a flight as:
#  - Less than 7 days before departure
#  - 7 or more days before departure
ticket_df['Purchase Status'] = np.where(ticket_df['Days until flight']<7,'Less than 7 days before departure','7 or more days before departure')

# Mimic the SUMIFS and AverageIFS functions by aggregating the previous requirements fields by each Flight and Class
output_df = ticket_df.groupby(['Flight','Class','Purchase Status']).agg(avg_daily_sales = ('Ticket Sales','mean'),sales = ('Ticket Sales','sum')).reset_index()
# Round all data to zero decimal places
output_df['avg_daily_sales'] = round(output_df['avg_daily_sales'],0)
output_df['sales'] = round(output_df['sales'],0)

# split into two dataframes and then join back together
less_than_7 = output_df.loc[output_df['Purchase Status'] == 'Less than 7 days before departure']
more_than_7 = output_df.loc[output_df['Purchase Status'] == '7 or more days before departure']

cols_to_keep = ['Flight','Class','avg_daily_sales','sales']
less_than_7 = less_than_7[cols_to_keep]
more_than_7 = more_than_7[cols_to_keep]

less_than_7.columns = ['Flight','Class','Avg. daily sales less than 7 days until the flight','Sales less than 7 days until the flight']
more_than_7.columns = ['Flight','Class','Avg. daily sales 7 days or more until the flight','Sales 7 days or more until the flight']

wide_ouput_df = pd.merge(less_than_7, more_than_7, on=['Flight','Class'], how='inner')

# Output the data
col_order = ['Flight','Class','Avg. daily sales 7 days or more until the flight','Avg. daily sales less than 7 days until the flight','Sales less than 7 days until the flight','Sales 7 days or more until the flight']
wide_ouput_df = wide_ouput_df[col_order]

wide_ouput_df.to_csv('prepped_data\\PD 2021 Wk 32 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
