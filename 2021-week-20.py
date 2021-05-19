# Preppin' Data 2021 Week 20
import pandas as pd
import numpy as np

# Load data
complaints = pd.read_csv('unprepped_data\\PD 2021 Wk 20 Input - Prep Air Complaints - Complaints per Day.csv')

# Create the mean and standard deviation for each Week

# Create the following calculations for each of 1, 2 and 3 standard deviations:
# - The Upper Control Limit (mean+(n*standard deviation))
# - The Lower Control Limit (mean-(n*standard deviation))
# - Variation (Upper Control Limit - Lower Control Limit)

# Join the original data set back on to these results 

# Assess whether each of the complaint values for each Department, Week and Date is within or outside of the control limits

# Output only Outliers

# Produce a separate output worksheet (or csv) for 1, 2 or 3 standard deviations and remove the irrelevant fields for that output.

print("data prepped!")
