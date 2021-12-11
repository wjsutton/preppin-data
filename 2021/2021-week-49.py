# Preppin' Data 2021 Week 49
import pandas as pd
import numpy as np
from datetime import datetime

# Load Data
# supply dateparse to read csv allows to dates to be formatted correctly
dateparse = lambda x: datetime.strptime(x, '%d/%m/%Y')
df = pd.read_csv('unprepped_data\\PD 2021 Wk 49 Input.csv', parse_dates=['Date'], date_parser=dateparse)

# Create the Employment Range field which captures the employees full tenure at the company in the MMM yyyy to MMM yyyy format. 
employ_df = df.groupby(['Name']).agg(date_min=('Date','min'),date_max=('Date','max')).reset_index()
employ_df['date_min'] = employ_df['date_min'].dt.strftime('%b %Y')
employ_df['date_max'] = employ_df['date_max'].dt.strftime('%b %Y')
employ_df['Employment Range'] = employ_df['date_min'].astype(str) +' to '+ employ_df['date_max'].astype(str)
del employ_df['date_min']
del employ_df['date_max']

# Work out for each year employed per person:
#  - Number of months they worked
#  - Their salary they will have received 
#  - Their sales total for the year
# For each Reporting Year (the individual year someone worked for us), calculate their cumulative months (called Tenure)
df['Reporting Year'] = df['Date'].dt.year
career_df = df.groupby(['Name','Reporting Year','Annual Salary']).agg(date_min=('Date','min'),date_max=('Date','max'),months_worked=('Date','count'),total_sales=('Sales','sum')).reset_index()
career_df['Salary Paid'] = career_df['Annual Salary'] * (career_df['months_worked'] / 12)

# use cumsum for running total
career_df['Tenure by End of Reporting Year'] = career_df['months_worked'].groupby(career_df['Name']).transform('cumsum')

# Add in employment range
career_df = pd.merge(career_df,employ_df,on='Name',how='inner')

# Determine the bonus payments the person will have received each year
#  - It's 5% of their sales total
career_df['Yearly Bonus'] = career_df['total_sales'] * 0.05

# Round Salary Paid and Yearly Bonus to two decimal places 
career_df['Salary Paid'] = round(career_df['Salary Paid'],2)
career_df['Yearly Bonus'] = round(career_df['Yearly Bonus'],2)

# Add Salary Paid and Yearly Bonus together to form Total Paid
career_df['Total Paid'] = career_df['Salary Paid'] + career_df['Yearly Bonus']

# Output the data
cols = ['Name','Employment Range','Reporting Year','Tenure by End of Reporting Year','Salary Paid','Yearly Bonus','Total Paid']
career_df = career_df[cols]

# Write to csv
career_df.to_csv('prepped_data\\PD 2021 Wk 49 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
