import pandas as pd
import math

#Highlights which logistic regression values were significant
def log_reg_results(log_reg_df: pd.DataFrame) -> str:
    log_reg_df['P-Val'] = log_reg_df['P-Val'].astype(str)
    risk_factors = 'Factors Associated with increased risk are '
    protective_factors = 'Factors with an associated cushioning effect are '
    mask_1 = (log_reg_df['P-Val'] == '<0.01') & (log_reg_df['LB'] > 1.0)
    mask_2 = (log_reg_df['P-Val'] == '<0.01') & (log_reg_df['UB'] < 1.0)
    df_risk = log_reg_df[mask_1].reset_index()
    df_cushion = log_reg_df[mask_2].reset_index()
    print(df_risk)
    print(df_cushion)
    for i in range(0, len(df_risk)):
        risk_factors += str(df_risk.loc[i, 'Ind_Var']) + '(OR ' + str(df_risk.loc[i, 'Coeff']) + ', P <0.01), '
    for j in range(0, len(df_cushion)):
        protective_factors += str(df_cushion.loc[j, 'Ind_Var']) + '(OR ' + str(df_cushion.loc[j, 'Coeff']) + ', P <0.01), '
    print(risk_factors)
    print(protective_factors)
    return risk_factors + protective_factors


#assume over same years
#assume upper and lower bounds match
#Returns where there were p<0.05 changes in year to year trends
def trends_results(trends_1:  pd.DataFrame) -> str:
    trends_1 = trends_1.reset_index()
    col_name_df = trends_1.columns[2]
    trend_str = f"There were significant (P<0.05) differences in the {col_name_df} intervention between the years of "
    for i in range(0, len(trends_1)-1):
        index = i + 1
        value_UB_1 = trends_1.loc[i, 'UB']
        value_UB_2 = trends_1.loc[index, 'UB']
        value_LB_1 = trends_1.loc[i, 'LB']
        value_LB_2 = trends_1.loc[index, 'LB']
        year_1 = trends_1.loc[i, 'Year']
        year_2 = trends_1.loc[index, 'Year']
        pop_est_1 = math.floor((value_UB_1 + value_LB_1) / 2)
        pop_est_2 = math.floor((value_UB_2 + value_LB_2) / 2)
        if (value_UB_1 > value_LB_2 or value_LB_1 < value_UB_2):
            if (not (str(year_1) in trend_str)):
                trend_str += f"{year_1} (N={pop_est_1} [{value_LB_1}, {value_UB_1}]) and {year_2} (N={pop_est_2} CI [{value_UB_2}, {value_LB_2}]), "
            else:
                trend_str += f"{year_1} and {year_2} (N={pop_est_2} [{value_LB_1}, {value_UB_2}]), "
    return trend_str

#Results in characteristic table which were significant with p<0.001 threshold
def characteristic_results(char_table: pd.DataFrame) -> str:
    
    name_var_col = char_table.columns[0]
    print(name_var_col)
    name_cohort_1 = char_table.columns[1]
    print(name_cohort_1)
    name_cohort_2 = char_table.columns[2]
    
    mask = char_table['P-Val'] == '<0.001'
    char_table = char_table[mask]
    char_table = char_table.reset_index()
    print(char_table)
    char_str = f"The cohort {name_cohort_1} differed from the second cohort \
        {name_cohort_2} in the  "
    for i in range(0, len(char_table)):
        Name_var = char_table.loc[i, name_var_col]
        Stat_C1 = char_table.loc[i, name_cohort_1]
        Stat_C2 = char_table.loc[i, name_cohort_2]
        
        char_str += f"with {Name_var} ({Stat_C1} vs. {Stat_C2}, P <0.001), "
    return char_str
