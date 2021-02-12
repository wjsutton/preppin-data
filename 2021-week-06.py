# Preppin' Data 2021 Week 06
import pandas as pd

# Load data
golf_df = pd.read_excel('unprepped_data\\PD 2021 Wk 6 Input - PGALPGAMoney2019.xlsx', engine='openpyxl', sheet_name = 'OfficialMoney')

# Answer these questions:
# 1. What's the Total Prize Money earned by players for each tour?
q1 = golf_df.groupby(['TOUR']).agg(total_prize_money = ('MONEY','sum')).reset_index()

# 2. How many players are in this dataset for each tour?
q2 = golf_df.groupby(['TOUR']).agg(number_of_players = ('PLAYER NAME','count')).reset_index()

# 3. How many events in total did players participate in for each tour?
q3 = golf_df.groupby(['TOUR']).agg(number_of_events = ('EVENTS','sum')).reset_index()

# 4. How much do players win per event? What's the average of this for each tour? 
golf_df['MONEY PER EVENT'] = golf_df['MONEY']/golf_df['EVENTS']
q4 = golf_df.groupby(['TOUR']).agg(avg_money_per_event = ('MONEY PER EVENT','mean')).reset_index()

# 5. How do players rank by prize money for each tour? What about overall? 
#    What is the average difference between where they are ranked within their tour compared to the overall rankings where both tours are combined? 
#    Here we would like the difference to be positive as you would presume combining the tours would cause a player's ranking to increase
golf_df['EARNINGS RANK BY TOUR'] = golf_df.groupby('TOUR')['MONEY'].rank(ascending=False)
golf_df['EARNINGS RANK OVERALL'] = golf_df['MONEY'].rank(ascending=False)
golf_df['DIFFERENCE IN EARNINGS RANK'] = golf_df['EARNINGS RANK OVERALL'] - golf_df['EARNINGS RANK BY TOUR']

q5 = golf_df.groupby(['TOUR']).agg(avg_difference_in_rank = ('DIFFERENCE IN EARNINGS RANK','mean')).reset_index()

# Combine the answers to these questions into one dataset
tour_df = q1
tour_df = tour_df.merge(q2, on='TOUR', how='inner')
tour_df = tour_df.merge(q3, on='TOUR', how='inner')
tour_df = tour_df.merge(q4, on='TOUR', how='inner')
tour_df = tour_df.merge(q5, on='TOUR', how='inner')

# Pivot the data so that we have a column for each tour, with each row representing an answer to the above questions
a = tour_df.melt(id_vars=['TOUR'], value_vars=['total_prize_money','number_of_players','number_of_events','avg_money_per_event','avg_difference_in_rank'])

# split lpga and pga into seperate dataframes then join later
lpga = a.loc[a['TOUR'] == 'LPGA']
pga = a.loc[a['TOUR'] == 'PGA']

lpga = lpga[['variable','value']]
pga = pga[['variable','value']]

# renaming columns
new_lpga_columns = lpga.columns.values
new_lpga_columns = ['Measure','LPGA']
lpga.columns  = new_lpga_columns

new_pga_columns = pga.columns.values
new_pga_columns = ['Measure','PGA']
pga.columns  = new_pga_columns

output = pga.merge(lpga, on='Measure', how='inner')

# Clean up the Measure field and create a new column showing the difference between the tours for each measure
# We're looking at the difference between the LPGA from the PGA, so in most instances this number will be negative
output['Difference between tours'] = output['LPGA'] - output['PGA']
output['Measure'] = ['Total Prize Money','Number of Players','Number of Events','Avg Money per Event','Avg Difference in Ranking']
output = output.reindex([4,3,1,2,0])

# Output
output.to_csv('prepped_data\\PD 2021 Wk 6 Output - Golf Tour KPIs.csv', index=False)

print("data prepped!")
