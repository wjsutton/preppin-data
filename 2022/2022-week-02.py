# Preppin' Data 2022 Week 02
import pandas as pd
import numpy as np

# Load csv
df = pd.read_csv('2022\\unprepped_data\\PD 2022 Wk 2 Input.csv')

# Removing any unnecessary fields (parental fields) will make this challenge easier to see what is happening at each step
del df['Parental Contact Name_1']
del df['Parental Contact Name_2']
del df['Preferred Contact Employer']
del df['Parental Contact']

# Format the pupil's name in First Name Last Name format (ie Carl Allchin)
df['Pupil Name'] = df['pupil first name'] + ' ' + df['pupil last name']

# Create the date for the pupil's birthday in calendar year 2022 (not academic year)
# convert date of birth to datetime
df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])

# replace year in birthday with 2021 if Sept-Dec or 2022 otherwise
df["This Year's Birthday"] = df['Date of Birth'].map(lambda x: x.replace(year=2021 if x.month >= 9 else 2022))

# Work out what day of the week the pupil's birthday falls on
df["Cake Needed On"] = df["This Year's Birthday"].dt.day_name()

# Remember if the birthday falls on a Saturday or Sunday, we need to change the weekday to Friday
df["Cake Needed On"] = np.where(np.isin(df["Cake Needed On"],['Saturday','Sunday']),'Friday',df["Cake Needed On"])

# Work out what month the pupil's birthday falls within
df["Month"] = df["This Year's Birthday"].dt.month_name()
df['Rows'] = 1

# Count how many birthdays there are on each weekday in each month
df['BDs per Weekday and Month'] = df.groupby(['Month','Cake Needed On'])['Rows'].transform(np.sum)

# Remove any unnecessary columns of data 
output_cols =['Pupil Name','Date of Birth',"This Year's Birthday","Month","Cake Needed On",'BDs per Weekday and Month']
df = df[output_cols]

# Output the data 
df.to_csv('2022\\prepped_data\\PD 2022 Wk 2 Output.csv', index=False)

print("data prepped!")
