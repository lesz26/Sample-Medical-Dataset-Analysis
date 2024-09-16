import pandas as pd
import polars as pl

#Get codes with associated counts ICD-10 CM (diagnosis) codes
def get_diagnosis_description_nums(df, df_description):
    df_description.rename(columns = {'CODE': 'I10_DX1'}, inplace = True)
    print(df_description.columns)
    df = df.iloc[:, 17:47]
    print(df.columns)
    val = df.groupby('I10_DX1').agg(count = ('I10_DX2', 'count'))
    val = val.reset_index()
    val = pd.merge(df_description, val,  on = 'I10_DX1', how = 'left')

    print(val)
    for i in range(2, 30):
        new_val = df.groupby('I10_DX' + str(i)).agg(count = ('I10_DX' + str(i + 1), 'count')).reset_index()
        print(val.head())
        print(new_val.head())
        new_val.columns = ['I10_DX1', 'count' + str(i)]
        val = pd.merge(val, new_val, how = 'left', on = 'I10_DX1')

    print(val)
    val.fillna(0.0, inplace = True)
    print(val.head())
    val['COUNT'] = val.iloc[:,6:33].sum(axis = 1)
    print(val.columns)

    val = val.sort_values(by = 'COUNT', ascending=False)
    val['COUNT'] = val['COUNT'].astype(int)
    print(val.head())
    new_val = val[['I10_DX1', 'COUNT', 'Description']]
    return new_val

#Get procedure code description numbers with associated count in subset
def get_proc_code_descript_nums(df, df_ps_10_codes: pd.DataFrame):
    df_ps_10_codes.rename(columns = {'CODE': 'I10_PR1'}, inplace = True)
    print(df_ps_10_codes.head())
    df = df.iloc[:, 54:69]
    print(df.columns)
    df = df.astype(str)
    print(df.dtypes)
    val = df.groupby('I10_PR1').agg(count = ('I10_PR2', 'count'))
    val = val.reset_index()

    print(val.head())
    val = pd.merge(df_ps_10_codes, val,  on = 'I10_PR1', how = 'left')
    print(val['count'].unique())
    print(val.head())

    for i in range(2, 16):
        new_val = df.groupby('I10_PR' + str(i)).agg(count = ('I10_PR' + str(i), 'count')).reset_index()
        new_val.columns = ['I10_PR1', 'count' + str(i)]
        val = pd.merge(val, new_val, how = 'left', on = 'I10_PR1')

    val.fillna(0.0, inplace = True)
    print(val.columns)
    val['COUNT'] = val.iloc[:,2:16].sum(axis = 1)
    val = val.sort_values(by = 'COUNT', ascending= False)
    val['COUNT'] = val['COUNT'].astype(int)
    print(val['COUNT'].unique())
    new_val = val[['I10_PR1', 'COUNT', 'Description']]
    return new_val

#Return assocatiated CPT description codes with associated counts
def get_cpt_descript_nums(df):
    df_cpt = pd.read_csv("C:\\Users\\zacha\\Desktop\\Research_CSV_Files\\CPT.csv")
    print(df_cpt.head())
    df = df[['cpt1', 'cpt2', 'cpt3', 'cpt4', 'cpt5',
             'cpt6', 'cpt7', 'cpt8', 'cpt9', 'cpt10',
             'cpt11', 'cpt12', 'cpt13', 'cpt14', 'cpt15',
             'cpt16', 'cpt17', 'cpt18', 'cpt19', 'cpt20',
             'cpt21', 'cpt22', 'cpt23', 'cpt24', 'cpt25',
             'cpt26', 'cpt27', 'cpt28', 'cpt29', 'cpt30',]]
    print(df.columns)
    df = df.astype(str)
    print(df.dtypes)
    val = df.groupby('cpt1').agg(count = ('I10_PR2', 'count'))
    val = val.reset_index()

    print(val.head())
    val = pd.merge(df_cpt, val,  on = 'cpt1', how = 'left')
    print(val['count'].unique())
    print(val.head())

    for i in range(2, 30):
        new_val = df.groupby('Icpt' + str(i)).agg(count = ('cpt' + str(i), 'count')).reset_index()
        new_val.columns = ['cpt', 'count' + str(i)]
        val = pd.merge(val, new_val, how = 'left', on = 'cpt')

    val.fillna(0.0, inplace = True)
    print(val.columns)
    val['COUNT'] = val.iloc[:,2:30].sum(axis = 1)
    val = val.sort_values(by = 'COUNT', ascending= False)
    val['COUNT'] = val['COUNT'].astype(int)
    print(val['COUNT'].unique())
    new_val = val[['cpt1', 'COUNT', 'Description']]
    return new_val