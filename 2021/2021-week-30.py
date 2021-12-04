# Preppin' Data 2021 Week 30
from numpy.lib.function_base import average
import pandas as pd
import numpy as np

# Load data
lift_df = pd.read_csv('unprepped_data\\PD 2021 Wk 30 Input.csv')

# Create a TripID field based on the time of day
#  - Assume all trips took place on 12th July 2021
lift_df['Year'] = 2021
lift_df['Month'] = 7
lift_df['Day'] = 12
lift_df['Trip_datetime'] = pd.to_datetime(lift_df[['Year', 'Month', 'Day', 'Hour', 'Minute']])

# sort by trip datetime and rename to TripID
lift_df = lift_df.reset_index()
lift_df = lift_df.sort_values(by=['Trip_datetime','index'])
lift_df = lift_df.rename(columns={'index':'TripID'})

# Calculate how many floors the lift has to travel between trips
#  - The order of floors is B, G, 1, 2, 3, etc.
lift_df['From_num'] = np.where(lift_df['From'] == 'B','-1',np.where(lift_df['From'] == 'G','0',lift_df['From']))
lift_df['To_num'] = np.where(lift_df['To'] == 'B','-1',np.where(lift_df['To'] == 'G','0',lift_df['To']))

# convert strings to int
lift_df['From_num'] = lift_df['From_num'].astype(int)
lift_df['To_num'] = lift_df['To_num'].astype(int)

lift_df['Floors_travelled'] = lift_df['From_num'].shift(-1) - lift_df['To_num']
lift_df['Floors_travelled'] = abs(lift_df['Floors_travelled'])

# Calculate which floor the majority of trips begin at - call this the Default Position
trip_df = pd.DataFrame(lift_df['From'].value_counts())
trip_df['Starting Floor'] = trip_df.index
trip_df.columns = ['Trips','Starting Floor']

default_position = trip_df[trip_df['Trips'] == trip_df['Trips'].max()]['Starting Floor']
default_position = default_position.iloc[0]

# If every trip began from the same floor, how many floors would the lift need to travel to begin each journey?
#  - e.g. if the default position of the lift were floor 2 and the trip was starting from the 4th floor, this would be 2 floors that the lift would need to travel
lift_df['default_position'] = default_position
lift_df['default_position_num'] = np.where(lift_df['default_position'] == 'B','-1',np.where(lift_df['default_position'] == 'G','0',lift_df['default_position']))
lift_df['default_position_num'] = lift_df['default_position_num'].astype(int)

# Note shift(-1) looks up the previous row in dataframe
lift_df['travel_from_default_position'] = lift_df['From_num'].shift(-1) - lift_df['default_position_num']
lift_df['travel_from_default_position'] = abs(lift_df['travel_from_default_position'])

# How does the average floors travelled between trips compare to the average travel from the default position?
output_df = pd.DataFrame({
    'Default Position': [default_position],
    'Avg travel from default position': [lift_df['travel_from_default_position'].mean()],
    'Avg travel between trips currently': [lift_df['Floors_travelled'].mean()]
})

output_df['Difference'] = output_df['Avg travel from default position'] - output_df['Avg travel between trips currently']

# round values
output_df['Avg travel from default position'] = round(output_df['Avg travel from default position'],2)
output_df['Avg travel between trips currently'] = round(output_df['Avg travel between trips currently'],2)
output_df['Difference'] = round(output_df['Difference'],2)

# Output the data
output_df.to_csv('prepped_data\\PD 2021 Wk 30 Output.csv', encoding="utf-8-sig", index=False)

print("data prepped!")
