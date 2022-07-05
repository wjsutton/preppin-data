# Preppin' Data 2022 Week 03
import pandas as pd
import numpy as np

# Input both data sets
students = pd.read_csv('2022\\unprepped_data\\PD 2022 Wk 1 Input.csv')
grades = pd.read_csv('2022\\unprepped_data\\PD 2022 Wk 3 Input.csv')

# Join the data sets together to give us the grades per student
df = pd.merge(students,grades,how='inner',left_on='id',right_on='Student ID')

# Remove the parental data fields, they aren't needed for the challenge this week
cols_to_remove = ['Parental Contact Name_1', 'Parental Contact Name_2','Preferred Contact Employer', 'Parental Contact', 'id']
cols_to_keep = [x for x in df.columns if x not in cols_to_remove]
df = df[cols_to_keep]

# Pivot the data to create one row of data per student and subject
# Rename the pivoted fields to Subject and Score 
df = df.melt(id_vars=['Student ID','pupil first name','pupil last name','gender','Date of Birth'], var_name='Subject', value_name='Score')

# Create an average score per student based on all of their grades
df["Student's Avg Score"] = df.groupby(['Student ID'])['Score'].transform('mean')

# Create a field that records whether the student passed each subject
# Pass mark is 75 and above in all subjects
df['Passed Subject'] = np.where(df['Score']>=75,1,0)

# Aggregate the data per student to count how many subjects each student passed
df = df.groupby(['Student ID','gender',"Student's Avg Score"]).agg(passed_subjects=('Passed Subject','sum')).reset_index()

# Round the average score per student to one decimal place
df = df.round({"Student's Avg Score": 1})

# Remove any unnecessary fields and output the data
df.rename( columns={'passed_subjects':'Passed Subjects','gender':'Gender'}, inplace=True )
col_order = ['Passed Subjects',"Student's Avg Score",'Student ID','Gender']
df = df[col_order]

# Writing data to csv
df.to_csv('2022\\python_scripts\\outputs\\PD 2022 Wk 3 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
