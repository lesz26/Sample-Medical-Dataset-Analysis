import pandas as pd
import polars as pl
import numpy as np
from scipy.stats import chisquare, ttest_ind


#takes in lazy df, 2 conditions for diagnosis (ICD-10 code), Creates column with a new name
def get_var_DX_Multiple(df: pl.DataFrame.lazy, array_conditions: list[str], new_name: str) -> pl.DataFrame.lazy:
    cols_dx = ['I10_DX1','I10_DX2','I10_DX3',
    'I10_DX4','I10_DX5','I10_DX6','I10_DX7','I10_DX8',
    'I10_DX9','I10_DX10','I10_DX11','I10_DX12','I10_DX13','I10_DX14',
    'I10_DX15','I10_DX16','I10_DX17','I10_DX18','I10_DX19',
    'I10_DX20','I10_DX21','I10_DX22','I10_DX23','I10_DX24',
    'I10_DX25','I10_DX26','I10_DX27','I10_DX28','I10_DX29','I10_DX30']
    
    df = df.with_columns(pl.when(pl.any_horizontal(pl.col(cols_dx).str.starts_with(array_conditions[0]), pl.col(cols_dx).str.starts_with(array_conditions[1]))).then(1.0).otherwise(0.0).alias(new_name))
    return df

#takes in lazy_df, 1 ICD-10 Condition, new column name
def get_variables_DX(df: pl.DataFrame.lazy, condition: str, new_name: str) -> pl.DataFrame.lazy:
    cols_dx = ['I10_DX1','I10_DX2','I10_DX3',
    'I10_DX4','I10_DX5','I10_DX6','I10_DX7','I10_DX8',
    'I10_DX9','I10_DX10','I10_DX11','I10_DX12','I10_DX13','I10_DX14',
    'I10_DX15','I10_DX16','I10_DX17','I10_DX18','I10_DX19',
    'I10_DX20','I10_DX21','I10_DX22','I10_DX23','I10_DX24',
    'I10_DX25','I10_DX26','I10_DX27','I10_DX28','I10_DX29','I10_DX30']
    df = df.with_columns(pl.when(pl.any_horizontal(pl.col(cols_dx).str.starts_with(condition))).then(1.0).otherwise(0.0).alias(new_name))
    return df

#accepts two ICD-10-PCS conditions and creates a new column 
def get_variables_PR(df: pl.DataFrame.lazy, condition: str, new_name: str) -> pl.DataFrame.lazy:
    cols = ['I10_PR1', 'I10_PR2', 'I10_PR3', 
    'I10_PR4', 'I10_PR5', 'I10_PR6', 
    'I10_PR7', 'I10_PR8', 'I10_PR9', 
    'I10_PR10', 'I10_PR11', 'I10_PR12',
    'I10_PR13', 'I10_PR14', 'I10_PR15']
    
    df = df.with_columns(pl.when(pl.any_horizontal(pl.col(cols).str.starts_with(condition))).then(1.0).otherwise(0.0).alias(new_name))
    return df

#Creates race yes no variables from pandas df
def race_get_dummies(df: pd.DataFrame) -> pd.DataFrame:
    temp = pd.get_dummies(df['RACE']).astype(float)
    df = pd.concat([df, temp], axis = 1)
    df.rename(columns = {1: 'WHITE', 2: 'BLACK', 3: 'HISPANIC', 
    4: 'ASIAN', 5: 'NATIVE_AMERICAN', 6: 'OTHER'}, inplace = True)
    return df

#Creates region yes no variables from region df
def region_get_dummies(df: pd.DataFrame) -> pd.DataFrame:
    df['NIS_STRATUM'] = np.floor((np.array(df['NIS_STRATUM']) / 1000))
    temp = pd.get_dummies(df['NIS_STRATUM']).astype(float)
    df = pd.concat([df, temp], axis = 1) 
    df.rename(columns = {1.0 :'NEW_ENGLAND', 2.0 :'MID_ATLANTIC',
    3.0:'EAST_NORTH_CENTRAL',  4.0 :'WEST_NORTH_CENTRAL', 5.0 : 'SOUTH_ATLANIC', 6.0 :'EAST_SOUTH_CENTRAL', 
    7.0:'WEST_SOUTH_CENTRAL', 8.0 :'MOUNTAIN', 9.0 : 'PACIFIC'}, inplace = True)
    return df

#Returns acute transfer-in, transfer-out, non-acute transfer-out as y-n variables
def group_TRAN_OUT(df: pd.DataFrame) -> pd.DataFrame:
    df['ACUTE_TRANSFER_OUT'] = 0.0
    mask = df['TRAN_OUT'] == 1
    df.loc[mask, 'ACUTE_TRANSFER_OUT'] = 1.0
    df['NON_ACUTE_TRANSFER_OUT'] = 0.0
    mask = df['TRAN_OUT'] == 2
    df.loc[mask, 'NON_ACUTE_TRANSFER_OUT'] = 1.0

    df['ACUTE_TRANSFER_IN'] = 0.0
    mask = df['TRAN_IN'] == 1
    df.loc[mask, 'ACUTE_TRANSFER_IN'] = 1.0
    df['NON_ACUTE_TRANSFER_IN'] = 0.0
    mask = df['TRAN_IN'] == 2
    df.loc[mask, 'NON_ACUTE_TRANSFER_IN'] = 1.0
    return df

#Returns time patient in hospital before operation
def time_before_op(df: pd.DataFrame) -> pd.DataFrame:
    df['TIME_OP'] = 0.0
    for i in range(1, 31):
        mask_1 = df['I10_DX' + str(i)].str.startswith('I7101')
        mask_2 = df['I10_DX' + str(i)].str.startswith('I7103')
        df.loc[mask_1 | mask_2, 'TIME_OP'] = df['PRDAY' + str(i)]
    return df
 
 #Manual chisquare test independence, (called p-test for purposes of this analysis)
 #Takes in yes counts, array lengths
def p_TEST(count_1, count_2, array_length_1, array_length_2):
    expected_1 = (count_1 + count_2) / (array_length_2 + array_length_1) * array_length_1
    expected_2 = (count_1 + count_2) / (array_length_2 + array_length_1) * array_length_2
    expected_array = np.array([expected_1, expected_2])
    observed_array = np.array([count_1, count_2])
    p = chisquare(f_obs = observed_array,f_exp=expected_array, ddof=0, axis=0)
    p_value = p[1]
    #If value <0.01 
    if (p_value < 0.001):
        return '<0.001'
    else:
        return round(p_value, 3) 
    
#Returns p-value forcContinous t-test for table 1 (characteristic)
def continous_t_test(df_1, df_2, column):
    p_val = ttest_ind(df_1[column], df_2[column], equal_var= False)[1]
    if (p_val > 0.001):
        p_val = round(p_val, 3)
    else:
        p_val = '<0.001'
    return p_val

#Returns payer information for surgery
def Pay_1(df: pd.DataFrame) -> pd.DataFrame : 
    temp = pd.get_dummies(df['PAY1'])
    temp.rename(columns = {1 : 'MEDICARE',
                          2: 'MEDICAID', 
                        3: 'PRIVATE_INSURANCE',
                        4: 'SELF_PAY',
                        5: 'NO_CHARGE'}, inplace = True)
    temp = temp[['MEDICARE', 'MEDICAID', 
                'PRIVATE_INSURANCE', 'SELF_PAY',
                'NO_CHARGE']]
    temp.replace({True: 1.0, False: 0.0}, inplace=True)
    df = pd.concat([df, temp], axis = 1)
    return df