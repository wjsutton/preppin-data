# Preppin' Data 2021 Week 15
import pandas as pd
import numpy as np

# Load data
menu = pd.read_excel('unprepped_data\\PD 2021 Wk 15 Input - Menu and Orders.xlsx', engine='openpyxl', sheet_name = 'MENU')
order = pd.read_excel('unprepped_data\\PD 2021 Wk 15 Input - Menu and Orders.xlsx', engine='openpyxl', sheet_name = 'Order')


def explode(df, lst_cols, fill_value='', preserve_index=False):
    # make sure `lst_cols` is list-alike
    if (lst_cols is not None
        and len(lst_cols) > 0
        and not isinstance(lst_cols, (list, tuple, np.ndarray, pd.Series))):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)
    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()
    # preserve original index values    
    idx = np.repeat(df.index.values, lens)
    # create "exploded" DF
    res = (pd.DataFrame({
                col:np.repeat(df[col].values, lens)
                for col in idx_cols},
                index=idx)
             .assign(**{col:np.concatenate(df.loc[lens>0, col].values)
                            for col in lst_cols}))
    # append those rows that have empty lists
    if (lens == 0).any():
        # at least one list in cells is empty
        res = (res.append(df.loc[lens==0, idx_cols], sort=False)
                  .fillna(fill_value))
    # revert the original index order
    res = res.sort_index()
    # reset index if requested
    if not preserve_index:        
        res = res.reset_index(drop=True)
    return res

# Modify the structure of the Menu table so we can have one column for:
#  - the Type (pizza, pasta, house plate), 
#  - the name of the plate, 
#  - ID, and Price

# reduce to individual data frames
pizza = menu.loc[:, 'Pizza':'Pizza ID']
pasta = menu.loc[:, 'Pasta':'Pasta ID']
house_plates = menu.loc[:, 'House Plates':'House Plates ID']

# rename all columns
columns = ['Plate','Price','ID']

pizza.columns = columns
pasta.columns = columns
house_plates.columns = columns

# add food type
pizza['Type'] = 'Pizza'
pasta['Type'] = 'Pasta'
house_plates['Type'] = 'House Plates'

# concat all data frames and remove NaNs
menu_df = pd.concat([pizza,pasta,house_plates])
menu_df = menu_df[menu_df.ID.notnull()]

order['ID'] = order.index
print(order)


#df.col.str.split(expand=True).head()
##s = order['Order'].str.split('-',expand=True).stack()
#combined = pd.merge(order,s, how='left', on=index)

#a = explode(order, ['Order'], fill_value='-')

a = pd.DataFrame(order['Order'].str.split('-',expand=True), index=order['ID'])
#a = pd.DataFrame(order['Order'].str.split('-').tolist(), index=order['Customer Name']).stack()
print(a)
a.columns = ['1','2','3','4']
print(a.columns)
a['ID'] = a.index

print(a)
a1 = a[['ID','1']]
a2 = a[['ID','2']]
print(a1)
#split_list = list(order['Order'].str.split('-'))
#print(split_list)
#better_split_list = [x if type(x) != np.float else [None,None] for x in split_list]
#print(better_split_list)
#a = explode(order.assign(var1=order['Order'].str.split('-')), 'Order')
# = pd.DataFrame(order['Order'].str.split('-').tolist(), index=order[['Customer Name', 'Order Date']]).stack()
#b = b.reset_index()[[0, 'var2']] # var1 variable is currently labeled 0
#b.columns = ['var1', 'var2'] # renaming var1

#pd.concat([Series(row['var2'], row['var1'].split(','))              
#                    for _, row in a.iterrows()]).reset_index()
#print(combined)
# Modify the structure of the Orders table to have each item ID in a different row 

# Join both tables 

# On Monday's we offer a 50% discount on all items. Recalculate the prices to reflect this

# For Output 1, we want to calculate the total money for each day of the week 

# For Output 2, we want to reward the customer who has made the most orders for their loyalty. 
# Work out which customer has ordered the most single items.


