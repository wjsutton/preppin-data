# Preppin' Data 2021 Week 46
import pandas as pd
import numpy as np

# Load data
book = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Book')
author = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Author')
info = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Info')
award = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Award')
checkouts = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Checkouts')
edition = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Edition')
publisher = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Publisher')
ratings = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Ratings')
series = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Series')
sales_q1 = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Sales Q1')
sales_q2 = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Sales Q2')
sales_q3 = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Sales Q3')
sales_q4 = pd.read_excel('unprepped_data\\PD 2021 Wk 46 Input.xlsx', sheet_name='Sales Q4')

# Union all the Sales data together to form one row per item in a sale
#  - This is the granularity of the data set throughout the whole challenge (56,350 rows)
total_sales = pd.concat([sales_q1,sales_q2,sales_q3,sales_q4])

# Join all other data sets in the workbook on to this data
#  - Never let the number of rows change
#     - You may need to disregard incomplete records or summarise useful data into a metric instead of including all the detail
book_sales_df = pd.merge(total_sales,edition, on = 'ISBN', how = 'left')
print(len(book_sales_df))

book_sales_df = pd.merge(book_sales_df,publisher, on = 'PubID', how = 'left')
print(len(book_sales_df))

ratings = ratings.groupby('BookID').agg({'Rating':'mean', 'ReviewID': 'count'}).reset_index()
ratings = ratings.rename(columns={'Rating':'avg_rating','ReviewID':'number_of_reviews'})
book_sales_df = pd.merge(book_sales_df,ratings, on = 'BookID', how = 'left')
print(len(book_sales_df))

checkouts = checkouts.groupby('BookID').agg({'CheckoutMonth':'count', 'Number of Checkouts': 'sum'}).reset_index()
checkouts = checkouts.rename(columns={'CheckoutMonth':'months_checked_out'})
book_sales_df = pd.merge(book_sales_df,checkouts, on = 'BookID', how = 'left')
print(len(book_sales_df))

info['BookID'] = info['BookID1'] + info['BookID2'].astype('str')
book_sales_df = pd.merge(book_sales_df,info, on = 'BookID', how = 'left')
print(len(book_sales_df))

book_sales_df = pd.merge(book_sales_df,book, on = 'BookID', how = 'left')
print(len(book_sales_df))

book_sales_df = pd.merge(book_sales_df,series, on = 'SeriesID', how = 'left')
print(len(book_sales_df))

book_sales_df = pd.merge(book_sales_df,author, on = 'AuthID', how = 'left')
print(len(book_sales_df))

award['Year Won'] = award['Year Won'].astype('str')
award = award.groupby('Title').agg([('Award Name', ', '.join),('Year Won', ', '.join)]).reset_index()
award.columns = ['Title','Award Name','Delete1','Delete2','Year Won']
award = award[['Title','Award Name','Year Won']]
book_sales_df = pd.merge(book_sales_df,award, on = 'Title', how = 'left')
print(len(book_sales_df))

# Remove any duplicate fields
# Remove the two fields created (in Prep at least) as the result of the Union:
#  - Table Names
#  - Sheet Names
book_sales_df = book_sales_df.drop(columns=['BookID1', 'BookID2'])

# Write to csv
book_sales_df.to_csv('prepped_data\\PD 2021 Wk 46 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
