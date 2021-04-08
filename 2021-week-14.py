# Preppin' Data 2021 Week 14
import pandas as pd
import numpy as np

# Load data
passengers = pd.read_excel('unprepped_data\\PD 2021 Wk 14 Input.xlsx', engine='openpyxl', sheet_name = 'Passenger List')
seats = pd.read_excel('unprepped_data\\PD 2021 Wk 14 Input.xlsx', engine='openpyxl', sheet_name = 'SeatList')
flights = pd.read_excel('unprepped_data\\PD 2021 Wk 14 Input.xlsx', engine='openpyxl', sheet_name = 'FlightDetails')
planes = pd.read_excel('unprepped_data\\PD 2021 Wk 14 Input.xlsx', engine='openpyxl', sheet_name = 'PlaneDetails')

# Assign a label for where each seat is located. 
# They are assigned as follows:
#  - A & F - Window Seats
#  - B & E - Middle Seats
#  - C & D - Aisle Seats 

#seats_df = pd.pivot_table(seats, values = 'passenger_number', index='Row', columns = ['A','B','C','D','E','F']).reset_index()
seats_df = pd.melt(seats, id_vars=['Row'], var_name='Position', value_name='passenger_number')
seats_df['seat_type'] = np.select(
    [
        seats_df['Position'] == 'A', 
        seats_df['Position'] == 'F',
        seats_df['Position'] == 'B', 
        seats_df['Position'] == 'E',
        seats_df['Position'] == 'C', 
        seats_df['Position'] == 'D'
    ], 
    [
        'Window Seats', 
        'Window Seats',
        'Middle Seats', 
        'Middle Seats',
        'Aisle Seats', 
        'Aisle Seats'
    ], 
    default='Unknown'
)


print(seats_df)
#print(flights)
#print(planes)

# Combine the Seat List and Passenger List tables. 

passengers_with_seats = pd.merge(passengers,seats_df,on='passenger_number',how='left')

print(passengers_with_seats)
# Parse the Flight Details so that they are in separate fields  

flights['[FlightID|DepAir|ArrAir|DepDate|DepTime]'] = flights['[FlightID|DepAir|ArrAir|DepDate|DepTime]'].str.replace('[','')
flights['[FlightID|DepAir|ArrAir|DepDate|DepTime]'] = flights['[FlightID|DepAir|ArrAir|DepDate|DepTime]'].str.replace(']','')
flights[['FlightID', 'DepAir','ArrAir','DepDate','DepTime']] = flights['[FlightID|DepAir|ArrAir|DepDate|DepTime]'].str.split('|', expand=True)

# Calculate the time of day for each flight. 
# They are assigned as follows: 
#  - Morning - Before 12:00 
#  - Afternoon - Between 12:00 - 18:00
#  - Evening - After 18:00

flights['DepHour'] = flights['DepTime'].str[0:2]
flights['DepHour'] = flights['DepHour'].astype(int)

flights['time_of_day'] = np.select(
    [
        flights['DepHour'].between(0, 11, inclusive=True), 
        flights['DepHour'].between(12, 17, inclusive=True), 
        flights['DepHour'].between(18, 23, inclusive=True) 
    ], 
    [
        'Morning', 
        'Afternoon',
        'Evening'
    ], 
    default='Unknown'
)

print(flights)
# Join the Flight Details & Plane Details to the Passenger & Seat tables. 
# We should be able to identify what rows are Business or Economy Class for each flight. 

planes[['BC_start','BC_end']] = planes['Business Class'].str.split('-', expand=True)
planes['BC_start'] = planes['BC_start'].astype(int)
planes['BC_end'] = planes['BC_end'].astype(int)

passengers_df = pd.merge(passengers_with_seats,planes,left_on='flight_number',right_on='FlightNo.',how='left')
passengers_df['flight_number'] = passengers_df['flight_number'].astype(str)
passengers_df = pd.merge(passengers_df,flights,left_on='flight_number',right_on='FlightID',how='left')
passengers_df['seat_class'] = np.where(passengers_df['Row'] <= passengers_df['BC_end'],'Business','Economy')
print(passengers_df)


# Answer the following questions: 
#  - What time of day were the most purchases made? We want to take a look at the average for the flights within each time period. 
#  - What seat position had the highest purchase amount? Is the aisle seat the highest earner because it's closest to the trolley?
#  - As Business Class purchases are free, how much is this costing us? 
#  - Bonus: If you have Tableau Prep 2021.1 or later, you can now output to Excel files. Can you combine all of the outputs into a single Excel workbook, with a different sheet for each output? 

# Outputs

output_df = passengers_df[['time_of_day','flight_number','seat_type','seat_class','purchase_amount']]
print(output_df)
# 1. What time of day were the most purchases made? (Avg per flight)

# avg purchase_amount by time of day
output_1 = output_df.groupby(['time_of_day','flight_number'],as_index=False)['purchase_amount'].agg('sum')
output_1 = output_1.groupby(['time_of_day'],as_index=False)['purchase_amount'].mean()
#output_1['Rank'] = output_1['purchase_amount'].rank(ascending=False)
#output_1['Rank'] = output_1['Rank'].astype(int)
#output_1 = output_1.sort_values(by='Rank', ascending=True).reset_index()
#del output_1['index']
#output_1 = output_1[['Rank','time_of_day','purchase_amount']]
#output_1.columns = ['Rank','Depart Time of Day','Avg per Flight']

# 2. What seat position had the highest purchase amount? 

# sum purchase_amount by seat_types
output_2 = output_df.groupby(['seat_type'],as_index=False)['purchase_amount'].agg('sum')

# 3. Business class purchases are free. How much is this costing us?

# sum purchase_amount by seat_class
output_3 = output_df.groupby(['seat_class'],as_index=False)['purchase_amount'].agg('sum')


print(output_1)
print(output_2)
print(output_3)