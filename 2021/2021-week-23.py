# Preppin' Data 2021 Week 23
import pandas as pd
import numpy as np

# Load data
airlines = pd.read_excel('unprepped_data\\PD 2021 Wk 23 Input - NPS Input.xlsx', sheet_name='Airlines')
prep_air = pd.read_excel('unprepped_data\\PD 2021 Wk 23 Input - NPS Input.xlsx', sheet_name='Prep Air')

# Combine Prep Air dataset with other airlines
airline_df = pd.concat([airlines,prep_air])

# Exclude any airlines who have had less than 50 customers respond
airline_df['total reviews'] = airline_df.groupby('Airline')['CustomerID'].transform('count')
airline_df = airline_df.loc[airline_df['total reviews'] >= 50]

# Classify customer responses to the question in the following way:
#   0-6 = Detractors 
#   7-8 = Passive
#   9-10 = Promoters
airline_df['Response Category'] =  np.select(
            [
                airline_df['How likely are you to recommend this airline?'] <= 6,
                airline_df['How likely are you to recommend this airline?'] <= 8,
                airline_df['How likely are you to recommend this airline?'] <= 10               
            ], 
            [
                'Detractors',
                'Passive',
                'Promoters'
            ], 
            default='Unknown'
        )

# Calculate the NPS for each airline
#   NPS = % Promoters - % Detractors
#   Note: I rounded the %s down to the nearest whole number, so if your answer differs slightly from mine then this could be why! 
nps = airline_df[['Airline','Response Category']]
nps = nps.groupby(['Airline','Response Category'], as_index=False).size()

# Pivot columns to rows
nps = nps.pivot(index = 'Airline', columns = 'Response Category', values = 'size').reset_index()
nps['Total'] = nps['Detractors'] + nps['Passive'] + nps['Promoters']

# Rounding % Promoters & % Detactors  before subtraction
nps['NPS Score % Rounded'] = np.floor((nps['Promoters']*100)/nps['Total']) - np.floor((nps['Detractors']*100)/nps['Total']) 

# Calculate the average and standard deviation of the dataset
airline_stats = nps['NPS Score % Rounded'].agg({'average':'mean',"standard deviation": 'std'})

# Take each airline's NPS and subtract the average, then divide this by the standard deviation
nps['Z-Score'] = (nps['NPS Score % Rounded'] - airline_stats['average'])/airline_stats['standard deviation']

# Filter to just show Prep Air's NPS along with their Z-Score
# Output the data
output_df = nps.loc[nps['Airline'] == 'Prep Air']
output_df = output_df[['Airline','NPS Score % Rounded','Z-Score']]
output_df.to_csv('prepped_data\\PD 2021 Wk 23 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
