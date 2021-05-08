# Preppin' Data 2021 Week 18
import pandas as pd
import numpy as np

# Load data
projects = pd.read_excel('unprepped_data\\PD 2021 Wk 18 Input.xlsx', engine='openpyxl', sheet_name = 'Sheet1')


# Workout the 'Completed Date' by adding on how many days it took to complete each task from the Scheduled Date

# Rename 'Completed In Days from Schedule Date' to 'Days Difference to Schedule'

# Your workflow will likely branch into two at this point:
# 1. Pivot Task to become column headers with the Completed Date as the values in the column
# You will need to remove some data fields to ensure the result of the pivot is a single row for each project, sub-project and owner combination. 
# Calculate the difference between Scope to Build time
# Calculate the difference between Build to Delivery time
# Pivot the Build, Deliver and Scope column to re-create the 'Completed Dates' field and Task field
# You will need to rename these


# # 2. You don't need to do anything else to this second flow

# Now you will need to:
# Join Branch 1 and Branch 2 back together 
# Hint: there are 3 join clauses for this join
# Calculate which weekday each task got completed on as we want to know whether these are during the weekend or not for the dashboard
# Clean up the data set to remove any fields that are not required.



# Writing data to csv
#output_df.to_csv('prepped_data\\PD 2021 Wk 18 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")