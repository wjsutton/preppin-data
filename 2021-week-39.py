# Preppin' Data 2021 Week 39
import pandas as pd
import numpy as np
import pandasql as ps

# Load data
bike_df = pd.read_csv('unprepped_data\\PD 2021 Wk 39 Input.csv')

# Create a Datetime field
bike_df['Datetime'] = pd.to_datetime(bike_df['Date'] + ' ' +bike_df['Time'])

# remove unnecessary columns
del bike_df['Date']
del bike_df['Time']
del bike_df['Data Type']

# Parse the Bike Type and Batch Status for each batch
bike_type = bike_df.loc[bike_df['Data Parameter'] == 'Bike Type']
bike_status = bike_df.loc[bike_df['Data Parameter'] == 'Batch Status']

reduce_columns = ['Batch No.','Data Value']

bike_type = bike_type[reduce_columns]
bike_status = bike_status[reduce_columns]

# Rename columns
bike_type.columns = ['Batch No.','Bike Type']
bike_status.columns = ['Batch No.','Batch Status']

type_and_status = pd.merge(bike_type,bike_status,on='Batch No.',how='inner')

# Parse the Actual & Target values for each parameter. 
targets = bike_df.loc[bike_df['Data Parameter'].str.contains('Target')]
actuals = bike_df.loc[bike_df['Data Parameter'].str.contains('Actual')]

targets['Data Parameter'] = targets['Data Parameter'].str.replace('Target ','')
actuals['Data Parameter'] = actuals['Data Parameter'].str.replace('Actual ','')

targets = targets.rename(columns={'Data Value': 'Target'})
actuals = actuals.rename(columns={'Data Value': 'Actual'})

targets['Actual'] = None 
actuals['Target'] = None 

col_order = ['Batch No.', 'Data Parameter', 'Actual','Target', 'Datetime']
targets_and_actuals = pd.concat([actuals[col_order],targets[col_order]])

# Identify what time each of the different process stage's took place. Each process stage is provided with a start time, and there is no overlap between stages. 
# Assume that the final process stage ends when the last update occurs.
# Output the data in a single table.
process_df = bike_df.loc[bike_df['Data Parameter'] == 'Name of Process Stage']
process_df = process_df.rename(columns={'Data Value': 'Name of Process Step'})
del process_df['Data Parameter']

# create order by ranking datetime reset at batch
process_df['Process Order'] = process_df['Datetime'].rank(ascending=True)
process_df['Previous'] = process_df['Process Order'] -1

process_df = pd.merge(process_df,process_df, left_on='Process Order',right_on='Previous',how='left')
process_df = process_df[['Batch No._x','Name of Process Step_x','Datetime_x','Datetime_y']]
process_df.columns = ['Batch No.','Name of Process Step','Start_time','End_time']

# Fill in Null with last datetime in dataset
last_datetime = max(bike_df['Datetime'])
process_df['End_time'] = process_df['End_time'].fillna(last_datetime)


# From https://stackoverflow.com/questions/30627968/merge-pandas-dataframes-where-one-value-is-between-two-others
# No pythonic way to join based on a value between two others so using SQL...

sqlcode = '''
SELECT
T.`Batch No.`
,P.`Name of Process Step`
,S.`Bike Type`
,S.`Batch Status`
,T.Datetime
,T.`Data Parameter`
,T.Target
,T.Actual
FROM targets_and_actuals AS T
INNER JOIN process_df AS P ON T.`Batch No.` = P.`Batch No.`
INNER JOIN type_and_status AS S ON T.`Batch No.` = S.`Batch No.`
WHERE P.Start_time<=T.Datetime AND P.End_time>=T.Datetime
ORDER BY T.Datetime ASC
'''

output_df = ps.sqldf(sqlcode,locals())

# Write to csv
output_df.to_csv('prepped_data\\PD 2021 Wk 39 Output.csv', index=False)

print("data prepped!")
