import pandas as pd
import numpy as np
import glob

preppin_data_challenges = pd.read_csv('meta\\challenge_list.csv')
preppin_data_scripts = glob.glob("20*.py")

script_df = pd.DataFrame()
script_df['Script'] = preppin_data_scripts
script_df['Week'] = script_df['Script'].str[:-3]

prep_df = pd.merge(preppin_data_challenges,script_df, on = 'Week', how = 'inner')
prep_df['Github URL'] = 'https://github.com/wjsutton/preppin-data/blob/main/' + prep_df['Script']
prep_df['Language'] = np.where(prep_df['Script'].str[-2:] == 'py','Python','Other')

prep_df['Challenge'] = '['+prep_df['Week'] + ']('+prep_df['Challenge']+')'
prep_df['Solution'] = '['+prep_df['Language'] + ']('+prep_df['Github URL']+')'
prep_df = prep_df.sort_values(by='Week', ascending=True)

prep_df = prep_df[['Challenge','Solution']]

prep_df['Table'] = '| ' + prep_df['Challenge'] + ' | ' + prep_df['Solution'] + ' |'

# Writing data to csv
prep_df.to_csv('meta\\completed_challenges_table.csv', encoding="utf-8-sig", index=False)

print(prep_df)