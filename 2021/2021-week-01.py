# Preppin' Data 2021 Week 01

import os
import pandas
import numpy 

# Load csv
data = pandas.read_csv('unprepped_data\\PD 2021 Wk 1 Input - Bike Sales.csv')

# Split the 'Store-Bike' into 'Store' and 'Bike'
data[['Store','Bike']] = data['Store - Bike'].str.split(' - ', expand=True)

# Clean up the 'Bike' field to: Mountain, Gravel, Road
data['Bike'] = data['Bike'].str.lower()
data['Bike'] = data['Bike'].str[0]
data['Bike'] = numpy.where(data['Bike']=='m','Mountain',numpy.where(data['Bike']=='r','Road','Gravel'))

# Create a 'Quarter' and 'Day of Month' fields
data['Date'] = pandas.to_datetime(data['Date'])
data['Quarter'] = data['Date'].dt.quarter 
data['Day of Month'] = data['Date'].dt.day 

# Remove the first 10 orders
data = data.loc[(data['Order ID'] >= 11)]

# Output the data as a csv
data = data.drop(['Store - Bike','Date'], axis=1)
data.to_csv('prepped_data\\PD 2021 Wk 1 Input - Bike Sales.csv', index=False)

print("data prepped!")
