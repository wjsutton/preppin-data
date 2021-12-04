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

# Create working dataframe
df = projects
df.columns =['week_number','commentary']

# explode project tasks into additional rows on '['
df = df.assign(commentary=df['commentary'].str.split(' \[')).explode('commentary')

# Convert string and all lookups to lowercase for ease of matching
df['commentary_lower'] = df['commentary'].str.lower()
proj_lookup['Project Code'] = proj_lookup['Project Code'].str.lower()
sub_proj_lookup['Sub-Project Code'] = sub_proj_lookup['Sub-Project Code'].str.lower()
# adding additional identifiers to lookups
task_lookup['Task Code'] = '-'+task_lookup['Task Code'].str.lower()
owner_lookup['Abbreviation'] = owner_lookup['Abbreviation'].str.lower()+'.'

# Convert week number to 'Week x'
df['Week'] = 'Week '+ df['week_number'].astype(str)

# Match Projects, Sub-Projects, Tasks and Owners to commentary and lookup tables
df['Project'] = np.where(df['commentary_lower'].str.contains(proj_lookup['Project Code'][0]),proj_lookup['Project'][0],
                np.where(df['commentary_lower'].str.contains(proj_lookup['Project Code'][1]),proj_lookup['Project'][1],
                np.where(df['commentary_lower'].str.contains(proj_lookup['Project Code'][2]),proj_lookup['Project'][2],'NA')))

df['Sub-Project'] = np.where(df['commentary_lower'].str.contains(sub_proj_lookup['Sub-Project Code'][0]),sub_proj_lookup['Sub-Project'][0],
                    np.where(df['commentary_lower'].str.contains(sub_proj_lookup['Sub-Project Code'][1]),sub_proj_lookup['Sub-Project'][1],'NA'))

df['Task'] = np.where(df['commentary_lower'].str.contains(task_lookup['Task Code'][0]),task_lookup['Task'][0],
             np.where(df['commentary_lower'].str.contains(task_lookup['Task Code'][1]),task_lookup['Task'][1],
             np.where(df['commentary_lower'].str.contains(task_lookup['Task Code'][2]),task_lookup['Task'][2],'NA')))

df['Name'] = np.where(df['commentary_lower'].str.contains(owner_lookup['Abbreviation'][0]),owner_lookup['Name'][0],
              np.where(df['commentary_lower'].str.contains(owner_lookup['Abbreviation'][1]),owner_lookup['Name'][1],
              np.where(df['commentary_lower'].str.contains(owner_lookup['Abbreviation'][2]),owner_lookup['Name'][2],
              np.where(df['commentary_lower'].str.contains(owner_lookup['Abbreviation'][3]),owner_lookup['Name'][3],'NA'))))

# Use Regex to find any days noted
df['Days Noted'] = df['commentary_lower'].str.extract(r'(\d+) day')

# Extract text after ']' 
df['Detail'] = df['commentary'].str.split('] ').str[1]

# delete unnecessary columns
del df['week_number']
del df['commentary']
del df['commentary_lower']

# Writing data to csv
df.to_csv('prepped_data\\PD 2021 Wk 19 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
