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
        'Window', 
        'Window',
        'Middle', 
        'Middle',
        'Aisle', 
        'Aisle'
    ], 
    default='Unknown'
)

# Combine the Seat List and Passenger List tables. 

passengers_with_seats = pd.merge(passengers,seats_df,on='passenger_number',how='left')

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

# Join the Flight Details & Plane Details to the Passenger & Seat tables. 
# We should be able to identify what rows are Business or Economy Class for each flight. 

planes[['BC_start','BC_end']] = planes['Business Class'].str.split('-', expand=True)
planes['BC_start'] = planes['BC_start'].astype(int)
planes['BC_end'] = planes['BC_end'].astype(int)

passengers_df = pd.merge(passengers_with_seats,planes,left_on='flight_number',right_on='FlightNo.',how='left')
passengers_df['flight_number'] = passengers_df['flight_number'].astype(str)
passengers_df = pd.merge(passengers_df,flights,left_on='flight_number',right_on='FlightID',how='left')
passengers_df['seat_class'] = np.where(passengers_df['Row'] <= passengers_df['BC_end'],'Business Class','Economy')

# Answer the following questions: 
#  - What time of day were the most purchases made? We want to take a look at the average for the flights within each time period. 
#  - What seat position had the highest purchase amount? Is the aisle seat the highest earner because it's closest to the trolley?
#  - As Business Class purchases are free, how much is this costing us? 
#  - Bonus: If you have Tableau Prep 2021.1 or later, you can now output to Excel files. Can you combine all of the outputs into a single Excel workbook, with a different sheet for each output? 

# Outputs

# filter to required columns and create dataframe of just ecomony class
output_df = passengers_df[['time_of_day','flight_number','seat_type','seat_class','purchase_amount']]
economy_df = output_df.loc[output_df['seat_class'] == 'Economy']

# 1. What time of day were the most purchases made? (Avg per flight)
# avg purchase_amount by time of day
output_1 = economy_df.groupby(['time_of_day','flight_number'],as_index=False)['purchase_amount'].agg('sum')
output_1 = output_1.groupby(['time_of_day'],as_index=False)['purchase_amount'].mean()
output_1['Rank'] = output_1['purchase_amount'].rank(ascending=False)
output_1['Rank'] = output_1['Rank'].astype(int)
output_1 = output_1.sort_values(by='Rank', ascending=True).reset_index()
del output_1['index']
output_1 = output_1[['Rank','time_of_day','purchase_amount']]
output_1['purchase_amount'] = output_1['purchase_amount'].round(2)
output_1.columns = ['Rank','Depart Time of Day','Avg per Flight']

# 2. What seat position had the highest purchase amount? 
# sum purchase_amount by seat_types
output_2 = economy_df.groupby(['seat_type'],as_index=False)['purchase_amount'].agg('sum')
output_2['Rank'] = output_2['purchase_amount'].rank(ascending=False)
output_2['Rank'] = output_2['Rank'].astype(int)
output_2 = output_2.sort_values(by='Rank', ascending=True).reset_index()
del output_2['index']
output_2 = output_2[['Rank','seat_type','purchase_amount']]
output_2.columns = ['Rank','Seat Position','Purchase Amount']

# 3. Business class purchases are free. How much is this costing us?
# sum purchase_amount by seat_class
output_3 = output_df.groupby(['seat_class'],as_index=False)['purchase_amount'].agg('sum')
output_3['Rank'] = output_3['purchase_amount'].rank(ascending=False)
output_3['Rank'] = output_3['Rank'].astype(int)
output_3 = output_3.sort_values(by='Rank', ascending=True).reset_index()
del output_3['index']
output_3 = output_3[['Rank','seat_class','purchase_amount']]
output_3.columns = ['Rank','Business Class','Purchase Amount']

# write data to Excel file
with pd.ExcelWriter('prepped_data\\PD 2021 Wk 14 Output.xlsx') as writer:  
    output_1.to_excel(writer, sheet_name='time_of_day_purchases', index=False)
    output_2.to_excel(writer, sheet_name='seat_position_purchases', index=False)
    output_3.to_excel(writer, sheet_name='seat_class_purchases', index=False)
    
print("data prepped!")