# Preppin' Data 2021 Week 20
import pandas as pd
import numpy as np

# Load data
complaints = pd.read_csv('unprepped_data\\PD 2021 Wk 20 Input - Prep Air Complaints - Complaints per Day.csv')

# Create the mean and standard deviation for each Week
weekly_stats = complaints.groupby(['Week'],as_index=False).apply(lambda s: pd.Series({ 
    "mean": s['Complaints'].mean(), 
    "std": s['Complaints'].std()}))

# Create the following calculations for each of 1, 2 and 3 standard deviations:
# - The Upper Control Limit (mean+(n*standard deviation))
# - The Lower Control Limit (mean-(n*standard deviation))
# - Variation (Upper Control Limit - Lower Control Limit)

# 1 Standard Deviation
weekly_stats['Upper Control Limit (1SD)'] = weekly_stats['mean']+(1*weekly_stats['std'])
weekly_stats['Lower Control Limit (1SD)'] = weekly_stats['mean']-(1*weekly_stats['std'])
weekly_stats['Variation (1SD)'] = weekly_stats['Upper Control Limit (1SD)'] - weekly_stats['Lower Control Limit (1SD)']

# 2 Standard Deviations
weekly_stats['Upper Control Limit (2SD)'] = weekly_stats['mean']+(2*weekly_stats['std'])
weekly_stats['Lower Control Limit (2SD)'] = weekly_stats['mean']-(2*weekly_stats['std'])
weekly_stats['Variation (2SD)'] = weekly_stats['Upper Control Limit (2SD)'] - weekly_stats['Lower Control Limit (2SD)']

# 3 Standard Deviations
weekly_stats['Upper Control Limit (3SD)'] = weekly_stats['mean']+(3*weekly_stats['std'])
weekly_stats['Lower Control Limit (3SD)'] = weekly_stats['mean']-(3*weekly_stats['std'])
weekly_stats['Variation (3SD)'] = weekly_stats['Upper Control Limit (3SD)'] - weekly_stats['Lower Control Limit (3SD)']


# Join the original data set back on to these results 
complaints_df = pd.merge(complaints, weekly_stats, on=['Week'], how='inner')

# Assess whether each of the complaint values for each Department, Week and Date is within or outside of the control limits

# making a new column for each outlier check
complaints_df['Outliers? (1SD)'] = np.where(complaints_df['Complaints'] > complaints_df['Upper Control Limit (1SD)'],'Outside',
    np.where(complaints_df['Complaints'] < complaints_df['Lower Control Limit (1SD)'],'Outside','Normal'))
complaints_df['Outliers? (2SD)'] = np.where(complaints_df['Complaints'] > complaints_df['Upper Control Limit (2SD)'],'Outside',
    np.where(complaints_df['Complaints'] < complaints_df['Lower Control Limit (2SD)'],'Outside','Normal'))
complaints_df['Outliers? (3SD)'] = np.where(complaints_df['Complaints'] > complaints_df['Upper Control Limit (3SD)'],'Outside',
    np.where(complaints_df['Complaints'] < complaints_df['Lower Control Limit (3SD)'],'Outside','Normal'))

# Output only Outliers
# Produce a separate output worksheet (or csv) for 1, 2 or 3 standard deviations and remove the irrelevant fields for that output.

# split dataframe into three, filtering on outliers
std_1_complaints = complaints_df.loc[complaints_df['Outliers? (1SD)'] == 'Outside']
std_2_complaints = complaints_df.loc[complaints_df['Outliers? (2SD)'] == 'Outside']
std_3_complaints = complaints_df.loc[complaints_df['Outliers? (3SD)'] == 'Outside']

# refine columns for dataframes
std_1_complaints = std_1_complaints[['Variation (1SD)','Outliers? (1SD)','Lower Control Limit (1SD)','Upper Control Limit (1SD)','std','mean','Date','Week','Complaints','Department']]
std_2_complaints = std_2_complaints[['Variation (2SD)','Outliers? (2SD)','Lower Control Limit (2SD)','Upper Control Limit (2SD)','std','mean','Date','Week','Complaints','Department']]
std_3_complaints = std_3_complaints[['Variation (3SD)','Outliers? (3SD)','Lower Control Limit (3SD)','Upper Control Limit (3SD)','std','mean','Date','Week','Complaints','Department']]

# standardise columns names
column_names = ['Variation','Outlier','Lower Control Limit','Upper Control Limit','Standard Deviation','Mean','Date','Week','Complaints','Department']
std_1_complaints.columns = column_names
std_2_complaints.columns = column_names
std_3_complaints.columns = column_names

# Writing data to csv
std_1_complaints.to_csv('prepped_data\\PD 2021 Wk 20 Output - 1 Standard Dev.csv', encoding="utf-8-sig", index=False)
std_2_complaints.to_csv('prepped_data\\PD 2021 Wk 20 Output - 2 Standard Dev.csv', encoding="utf-8-sig", index=False)
std_3_complaints.to_csv('prepped_data\\PD 2021 Wk 20 Output - 3 Standard Dev.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
