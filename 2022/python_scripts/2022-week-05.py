# Preppin' Data 2022 Week 05
import pandas as pd
import numpy as np

# Input data
grades = pd.read_csv('2022\\unprepped_data\\PD 2022 Wk 3 Input.csv')
df = grades.melt(id_vars='Student ID', var_name='Subject', value_name='Score')

# Divide the students grades into 6 evenly distributed groups (have a look at 'Tiles' functionality in Prep)
#  - By evenly distributed, it means the same number of students gain each grade within a subject
# Convert the groups to two different metrics:
#  - The top scoring group should get an A, second group B etc through to the sixth group who receive an F
#  - An A is worth 10 points for their high school application, B gets 8, C gets 6, D gets 4, E gets 2 and F gets 1.
df['Group'] = df.groupby(['Subject'])['Score'].rank(method='first').transform(pd.qcut,q=6, labels=['F','E','D','C','B','A'])

points_dict = {'A':10,'B':8,'C':6,'D':4,'E':2,'F':1}
df['points'] = df['Group'].replace(points_dict)
df['points'] = df['points'].astype(int)

# Determine how many high school application points each Student has received across all their subjects 
df['total_points'] = df.groupby(['Student ID'])['points'].transform('sum')

# Work out the average total points per student by grade 
#  - ie for all the students who got an A, how many points did they get across all their subjects
df['avg_points_per_grade'] = df.groupby(['Group'])['total_points'].transform('mean')

# Take the average total score you get for students who have received at least one A and remove anyone who scored less than this. 
students_with_an_a = df[df['Group']=='A']
threshold_a = students_with_an_a['avg_points_per_grade'].min()

df = df[df['total_points'] >= threshold_a]

# Remove results where students received an A grade (requirement updated 2/2/22)
df = df[df['Group'] != 'A']

df['points_without_a'] = df.groupby(['Student ID'])['points'].transform('sum')

# How many students scored more than the average if you ignore their As?
print(df[df['points_without_a'] >= threshold_a]['Student ID'].nunique())
# Output the data

# Writing data to csv
df.to_csv('2022\\python_scripts\\outputs\\PD 2022 Wk 5 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
