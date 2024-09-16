import matplotlib.pyplot as plt
import pandas as pd
from Create_Columns import continous_t_test, p_TEST


#Get variables and create characteristic table change for use case
def characteristic_table(df: pd.DataFrame, cohort_sep: str) -> pd.DataFrame: 
    #list continous and categorical variables, switch for use case
    list_categorical = ['AGE', 'FEMALE',
    'WHITE','BLACK','HISPANIC','ASIAN','NATIVE_AMERICAN','NEW_ENGLAND',
    'MID_ATLANTIC', 'EAST_NORTH_CENTRAL','WEST_NORTH_CENTRAL',
    'SOUTH_ATLANIC','EAST_SOUTH_CENTRAL', 'WEST_SOUTH_CENTRAL',
    'MOUNTAIN','PACIFIC', 'DIED']

    list_c = ['AGE', 'PL_NCHS', 'LOS']
    mask = df[cohort_sep] == 1.0

    df_BS = df[mask]
    df_NBS = df[~mask]
    length_BS = len(df_BS)
    length_NBS = len(df_NBS)
    print(length_BS)
    print(length_NBS)
    df_char = pd.DataFrame({'Variable': [], 'Cohort with ' + cohort_sep  
                            + '(N=' + str(len(df_BS)) + ')': [], 
                              'Cohort without ' + cohort_sep + '(N=' +
                                str(len(df_NBS)) + ')': [],
                              'P-Val': []})
    for i in range(0, len(list_categorical)):  
        val_count_NBS = int(df_NBS[list_categorical[i]].sum())
        val_count_BS = int(df_BS[list_categorical[i]].sum())
        pct_NBS = round((val_count_NBS/ len(df_NBS)) * 100, 2)
        pct_BS = round((val_count_BS/ len(df_BS)) * 100, 2)
        p_val =  p_TEST(val_count_BS, val_count_NBS, length_BS, length_NBS)
        temp = pd.DataFrame({'Variable': [list_categorical[i]],
                            'Cohort with ' + cohort_sep  + '(N=' +
                              str(len(df_BS)) + ')': [str(val_count_BS) +
                             ' (' + str(pct_BS) + '%)'], 
                            'Cohort without ' + cohort_sep + '(N=' + 
                            str(len(df_NBS)) + ')': [str(val_count_NBS) + ' (' + str(pct_NBS) + '%)'], 
                            'P-Val': [p_val]})
        df_char = pd.concat([df_char, temp], axis = 0)

    for j in range(0, len(list_c)):
        mn_BS = round(df_BS[list_c[j]].mean(), 2)
        std_BS = round(df_BS[list_c[j]].std(), 2)
        mn_NBS = round(df_NBS[list_c[j]].mean(), 2)
        std_NBS = round(df_NBS[list_c[j]].std(), 2) 
        p_val = continous_t_test(df_BS, df_NBS, list_c[j])
        temp = pd.DataFrame({'Variable': [list_c[j]],
                            'Cohort with ' + cohort_sep  +
                              '(N=' + str(len(df_BS)) + 
                              ')': [str(mn_BS) + ' (' + str(std_BS) + ')'], 
                            'Cohort without ' +
                              cohort_sep + '(N=' + str(len(df_NBS)) + 
                              ')': [str(mn_NBS) + ' (' + str(std_NBS) + ')'], 
                            'P-Val': [p_val]})
        df_char = pd.concat([df_char, temp], axis = 0)
    return df_char