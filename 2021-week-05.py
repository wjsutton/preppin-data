# Preppin' Data 2021 Week 05
import pandas
import numpy 

# Load csv
data = pandas.read_csv('unprepped_data\\PD 2021 Wk 5 Input.csv')

# For each Client, work out who the most recent Account Manager is
account_managers = data[['Client ID','Account Manager','From Date']]
latest_acc_manager = account_managers.groupby('Client ID')['From Date'].max()
latest_acc_manager = latest_acc_manager.to_frame().reset_index()

# joining latest client id to account managers dataframe to get latest account manager
latest_acc_manager = latest_acc_manager.merge(account_managers, on=['Client ID','From Date'], how='left')
latest_acc_manager = latest_acc_manager.drop_duplicates()

# Filter the data so that only the most recent Account Manager remains
# Be careful not to lose any attendees from the training sessions!
account_manager_lookup = latest_acc_manager[['Client ID','Account Manager']]
# renaming columns
aml_columns = account_manager_lookup.values
new_aml_columns = ['Client ID','Latest Account Manager']
account_manager_lookup.columns  = new_aml_columns

# joining latest account manager lookup as an extra column to source data then filtering account managers
df = data.merge(account_manager_lookup, on='Client ID', how='inner')
df = df.loc[df['Account Manager'] == df['Latest Account Manager']]

# In some instances, the Client ID has changed along with the Account Manager. Ensure only the most recent Client ID remains
# making lookup and spliting training to get date of the session
clients = data[['Training','Contact Email','Client ID']]
clients[['Session', 'Date']] = clients['Training'].str.split(' - ',expand=True)

latest_client_session = clients.groupby('Contact Email')['Date'].max()
latest_client_session = latest_client_session.to_frame().reset_index()

# inner join to get latest client id
latest_client_id = latest_client_session.merge(clients, on=['Contact Email','Date'], how='inner')
latest_client_id = latest_client_id['Client ID'].drop_duplicates()

# inner join on source data to filter for latest client ids
df = df.merge(latest_client_id, on='Client ID', how='inner')

# Output the data
df = df[['Training','Contact Email','Contact Name','Client','Client ID','Account Manager','From Date']]

# writing data to csv
df.to_csv('prepped_data\\PD 2021 Wk 5 Output.csv', index=False)

print("data prepped!")
