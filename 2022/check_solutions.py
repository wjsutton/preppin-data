## Check Solutions

import glob
import pandas as pd

def add_week_number(x):
    df = pd.DataFrame()
    df['link'] = x
    df['week'] = df['link'].str.extract('(W[K|k][ ]*[\d]+)')
    df['week'] = df['week'].str.extract('(\d+)')
    return(df)

correct_solutions = glob.glob("2022\\solutions\\*")
python_solutions = glob.glob("2022\\python_scripts\\outputs\\*")
alteryx_solutions = glob.glob("2022\\alteryx_workflows\\outputs\\*")
tab_prep_solutions = glob.glob("2022\\tableau_prep_flows\\outputs\\*")

solution_df = add_week_number(correct_solutions)
python_df = add_week_number(python_solutions)
alteryx_df = add_week_number(alteryx_solutions)
tab_prep_df = add_week_number(tab_prep_solutions)

solution_df = solution_df.rename(columns={'link':'answer'})
python_df = python_df.rename(columns={'link':'python'})
alteryx_df = alteryx_df.rename(columns={'link':'alteryx'})
tab_prep_df = tab_prep_df.rename(columns={'link':'tab_prep'})

solution_df = pd.merge(solution_df,python_df,how='left',on='week')
solution_df = pd.merge(solution_df,alteryx_df,how='left',on='week')
solution_df = pd.merge(solution_df,tab_prep_df,how='left',on='week')

check_python = solution_df[solution_df['python'].notnull()]
print('Python challenges...')
for i in range(0,len(check_python)):
    answer = pd.read_csv(check_python['answer'][i])
    python = pd.read_csv(check_python['python'][i])
    python = python[list(answer)]
    df_diff = pd.concat([answer,python]).drop_duplicates(keep=False)
    print('Week '+str(i+1)+', Differences: '+str(len(df_diff)))
print('\n')

check_alteryx = solution_df[solution_df['alteryx'].notnull()]
print('Alteryx challenges...')
for i in range(0,len(check_alteryx)):
    answer = pd.read_csv(check_alteryx['answer'][i])
    alteryx = pd.read_csv(check_alteryx['alteryx'][i])
    alteryx = alteryx[list(answer)]
    df_diff = pd.concat([answer,alteryx]).drop_duplicates(keep=False)
    print('Week '+str(i+1)+', Differences: '+str(len(df_diff)))
print('\n')

check_tab_prep = solution_df[solution_df['tab_prep'].notnull()]
print('Tableau Prep challenges...')
for i in range(0,len(check_tab_prep)):
    answer = pd.read_csv(check_tab_prep['answer'][i])
    tab_prep = pd.read_csv(check_tab_prep['tab_prep'][i])
    tab_prep = tab_prep[list(answer)]
    df_diff = pd.concat([answer,tab_prep]).drop_duplicates(keep=False)
    print('Week '+str(i+1)+', Differences: '+str(len(df_diff)))
print('\n')
