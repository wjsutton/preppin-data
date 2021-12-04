# Preppin' Data 2021 Week 12
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import re

# create pattern searcher function
# from: https://stackoverflow.com/questions/17972938/check-if-a-string-in-a-pandas-dataframe-column-is-in-a-list-of-strings
def pattern_searcher(search_str:str, search_list:str):

    search_obj = re.search(search_list, search_str)
    if search_obj :
        return_str = search_str[search_obj.start(): search_obj.end()]
    else:
        return_str = 'NA'
    return return_str

# Load data
tourism = pd.read_csv('unprepped_data\\PD 2021 Wk 12 Input - Tourism Input.csv')

# Pivot all of the month fields into a single column 
# Rename the fields and ensure that each field has the correct data type
tourism_df = tourism.melt(id_vars=tourism.columns[:4], var_name='Month',value_name='Values')

# Filter out the nulls 
tourism_df = tourism_df.loc[tourism_df['Values'] != 'na']

# Filter our dataset so our Values are referring to Number of Tourists
tourism_df = tourism_df.loc[tourism_df['Unit-Detail'] == 'Tourists']
tourism_df['Values'] = tourism_df['Values'].astype(int)

# Our goal now is to remove all totals and subtotals from our dataset so that only the lowest level of granularity remains. 
# Currently we have Total > Continents > Countries, but we don't have data for all countries in a continent, 
# so it's not as simple as just filtering out the totals and subtotals. Plus in our Continents level of detail, 
# we also have The Middle East and UN passport holders as categories. 
# If you feel confident in your prep skills, this (plus the output) should be enough information to go on, 
# but otherwise read on for a breakdown of the steps we need to take:
# - Filter out Total tourist arrivals
tourism_df = tourism_df.loc[tourism_df['Series-Measure'] != 'Total tourist arrivals']

# - Split our workflow into 2 streams: Continents and Countries (Hint: the hierarchy field will be useful here)
continents_df = tourism_df.loc[tourism_df['Hierarchy-Breakdown'] ==  'Real Sector / Tourism / Tourist arrivals']
countries_df = tourism_df.loc[tourism_df['Hierarchy-Breakdown'] !=  'Real Sector / Tourism / Tourist arrivals'] 

# - Split out the Continent and Country names from the relevant fields 
continents = ['Europe','Asia','Africa','Americas','Oceania','Middle East','UN passport holders and others']
countries =['Germany','Italy','Russia','United Kingdom','China','India','France','Australia','United States']

continents_pattern = '|'.join(continents)
countries_pattern = '|'.join(countries)
 
continents_df['Continent']  = continents_df['Series-Measure'].apply(lambda x: pattern_searcher(search_str=x, search_list=continents_pattern))
countries_df['Continent']  = countries_df['Hierarchy-Breakdown'].apply(lambda x: pattern_searcher(search_str=x, search_list=continents_pattern))
countries_df['Country']  = countries_df['Series-Measure'].apply(lambda x: pattern_searcher(search_str=x, search_list=countries_pattern))

# - Aggregate our Country stream to the Continent level 
country_agg = countries_df.groupby(['Continent','Month'],as_index=False)['Values'].agg('sum')
country_agg.columns =['Continent','Month','Country_Values']

# - Join the two streams together and work out how many tourists arrivals there are that we don't know the country of 
stream_join = pd.merge(continents_df,country_agg, on=['Continent','Month'], how='left')
stream_join['difference'] = stream_join['Values'] - stream_join['Country_Values']

# - Add in a Country field with the value "Unknown" 
stream_join['Country'] = 'Unknown'

# - Union this back to here we had our Country breakdown 
df1 = countries_df[['Month','Continent','Country','Values']]
df2 = stream_join[['Month','Continent','Country','difference']]
df2.columns = ['Month','Continent','Country','Values']

output_df = pd.concat([df1,df2])

# Output the data
output_df.columns = ['Month','Breakdown','Country','Number of Tourists']

# writing data to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 12 Output - Tourists.csv', index=False)

print("data prepped!")