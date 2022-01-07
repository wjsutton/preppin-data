# Preppin' Data 2022 Week 01
import pandas as pd

# Load csv
df = pd.read_csv('2022\\unprepped_data\\PD 2022 Wk 1 Input.csv')

# Form the pupil's name correctly for the records in the format Last Name, First Name 
df["Pupil's Name"] = df['pupil last name'] + ', ' + df['pupil first name']

# Form the parental contact's name in the same format as the pupil's 
#  - The Parental Contact Name 1 and 2 are the first names of each parent.
#  - Use parental contact column to select which parent first name to use along with the pupil's last name
df['Parental Contact Full Name'] = df['pupil last name'] + ', ' + df['Parental Contact Name_1']

# Create the email address to contact the parent using the format Parent First Name.Parent Last Name@Employer.com
df['Parental Contact Email Address'] = df['Parental Contact Name_1'] + '.' + df['pupil last name'] + '@' + df['Preferred Contact Employer'] + '.com'

# Create the academic year the pupils are in 
#  - Each academic year starts on 1st September.
#  - Year 1 is anyone born after 1st Sept 2014 
#  - Year 2 is anyone born between 1st Sept 2013 and 31st Aug 2014 etc

# convert date of birth to datetime
df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])
# then return year, but if the month is earlier than Sept return year -1 to place academic year, deduct from 2015 to get academic year
df['Academic Year'] = 2015 - df['Date of Birth'].map(lambda x: x.year if x.month > 9 else x.year-1)

# Remove any unnecessary columns of data 
output_cols = ["Academic Year","Pupil's Name","Parental Contact Full Name","Parental Contact Email Address"]
df = df[output_cols]

# Output the data 
df.to_csv('2022\\prepped_data\\PD 2022 Wk 1 Output.csv', index=False)

print("data prepped!")
