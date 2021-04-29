# Preppin' Data 2021 Week 17
import pandas as pd
import numpy as np

# Load data
employee_log = pd.read_excel('unprepped_data\\PD 2021 Wk 17 Input - Preppin Data Challenge.xlsx', engine='openpyxl', sheet_name = 'Sheet1')

# Remove the ‘Totals’ Rows
# Pivot Dates to rows and rename fields 'Date' and 'Hours'
# Split the ‘Name, Age, Area of Work’ field into 3 Fields and Rename
# Remove unnecessary fields
# Remove the row where Dan was on Annual Leave and check the data type of the Hours Field.
# Total up the number of hours spent on each area of work for each date by each employee.

# First we are going to work out the avg number of hours per day worked by each employee
# Calculate the total number of hours worked and days worked per person
# Calculate the avg hours and remove unnecessary fields.

# Now we are going to work out what % of their day (not including Chats) was spend on Client work.
# Filter out Work related to Chats.
# Calculate total number of hours spent working on each area for each employee
# Calculate total number of hours spent working on both areas together for each employee
# Join these totals together
# Calculate the % of total and remove unnecessary fields
# Filter the data to just show Client work
# Join to the table with Avg hours to create your final output

# Output the data

# Writing data to csv

print("data prepped!")