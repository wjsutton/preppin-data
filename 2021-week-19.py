# Preppin' Data 2021 Week 19
import pandas as pd
import numpy as np

# Load data
projects = pd.read_excel('unprepped_data\\PD 2021 Wk 19 Input.xlsx', engine='openpyxl', sheet_name = 'Project Schedule Updates')
proj_lookup = pd.read_excel('unprepped_data\\PD 2021 Wk 19 Input.xlsx', engine='openpyxl', sheet_name = 'Project Lookup Table')
sub_proj_lookup = pd.read_excel('unprepped_data\\PD 2021 Wk 19 Input.xlsx', engine='openpyxl', sheet_name = 'Sub-Project Lookup Table')
task_lookup = pd.read_excel('unprepped_data\\PD 2021 Wk 19 Input.xlsx', engine='openpyxl', sheet_name = 'Task Lookup Table')
owner_lookup = pd.read_excel('unprepped_data\\PD 2021 Wk 19 Input.xlsx', engine='openpyxl', sheet_name = 'Owner Lookup Table')

# There are lots of different ways you can do this challenge so rather than a step-by-step set of requirements, 
# feel free to create each of these data fields in whatever order you like:
# - 'Week' with the word week and week number together 'Week x' 
# - 'Project' with the full project name
# - 'Sub-Project' with the full sub-project name
# - 'Task' with the full type of task
# - 'Name' with the owner of the task's full name (Week 18's output can help you check these if needed) 
# - 'Days Noted' some fields have comments that say how many days tasks might take. 
#    This field should note the number of days mentioned if said in the comment otherwise leave as a null. 
# - 'Detail' the description from the system output with the project details in the [ ] 

# Output the file

# Writing data to csv
#output.to_csv('prepped_data\\PD 2021 Wk 19 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")