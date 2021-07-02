
#from inspect import getmembers, isfunction
import pandas as pd
import numpy as np
from pandas import DataFrame as df
import glob

preppin_data_scripts = glob.glob("20*.py")

pandas_df = pd.DataFrame()
pandas_df['Function'] = dir(pd)
pandas_df['Package'] = 'Pandas'

dataframe_df = pd.DataFrame()
a = set(dir(df))
b = set(dir(np))
c = list(a - b)
print(c)
dataframe_df['Function'] = c
dataframe_df['Package'] = 'Pandas DataFrame'

numpy_df = pd.DataFrame()
numpy_df['Function'] = dir(np)
numpy_df['Package'] = 'Numpy'

package_df = pd.concat([pandas_df,dataframe_df,numpy_df])
package_df['Search Terms'] = '.' + package_df['Function'] + '('

search_terms = package_df['Search Terms'].to_list()

for s in range(len(preppin_data_scripts)):
    print(preppin_data_scripts[s])
    with open(preppin_data_scripts[s], encoding='utf-8') as f:
        lines = f.read()

    functions = []

    for i in range(len(search_terms)):
        n = search_terms[i] in lines
        functions.append(n)

    usage_df = pd.DataFrame()
    usage_df['Search Terms'] = search_terms
    usage_df['File'] = preppin_data_scripts[s]
    usage_df['Used'] = functions

    usage_df = usage_df.loc[usage_df['Used'] == True]

    if s == 0:
        output_df = usage_df
    else:
        output_df = pd.concat([output_df,usage_df])

output_df = pd.merge(package_df,output_df,on = 'Search Terms', how = 'inner')

output_df['Github link'] = '[W' + output_df['File'].str[10:12] +'](https://github.com/wjsutton/preppin-data/blob/main/'+output_df['File'] + ')'

output_df['Github links'] = output_df[['Package','Function','Github link']].groupby(['Package','Function'])['Github link'].transform(lambda x: ', '.join(x))
output_df = output_df.sort_values(by=['Package','Function'], ascending=[True,True]).reset_index()
output_df = output_df[['Package','Function','Github links']].drop_duplicates()

output_df.to_csv('functions_used.csv', encoding="utf-8-sig", index=False)
print(output_df)


with open("README.md", "r+") as f:
     old = f.read() # read everything in the file
     f.seek(0) # rewind
     f.write("new line\n" + old) # write the new line before