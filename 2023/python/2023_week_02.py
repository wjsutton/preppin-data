# Preppin' Data 2023 Week 02

# load packages
import pandas as pd

# Input the data
transct_df = pd.read_csv('2023\\unprepped_data\\PD 2023 Wk 2 Transactions.csv')
swift_df = pd.read_csv('2023\\unprepped_data\\PD 2023 Wk 2 Swift Codes.csv')

# In the Transactions table, there is a Sort Code field which contains dashes. 
# We need to remove these so just have a 6 digit string
transct_df['Sort Code'] = transct_df['Sort Code'].str.replace('-','',regex=False)

# Use the SWIFT Bank Code lookup table to bring in additional information 
# about the SWIFT code and Check Digits of the receiving bank account
df = transct_df.merge(swift_df, how = 'inner', on = 'Bank')

# Add a field for the Country Code
# Hint: all these transactions take place in the UK so the Country Code should be GB
df['Country Code'] = 'GB'


# Create the IBAN as above
# Hint: watch out for trying to combine sting fields with numeric fields - check data types
df['IBAN'] = df['Country Code'] + df['Check Digits'] + df['SWIFT code'] +df['Sort Code'] + df['Account Number'].astype(str)

# Remove unnecessary fields
output_df = df[['Transaction ID','IBAN']]

# Output the data
output_df.to_csv('2023\\python\\outputs\\pd2023wk02_output.csv',index=False)