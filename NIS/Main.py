import polars as pl
import pandas as pd
import statsmodels.api as sm

from Subset_NIS import Subset_Diagnosis, Subset_Procedure
from Create_Columns import get_variables_DX, get_var_DX_Multiple, get_variables_PR
from Create_Columns import Pay_1, region_get_dummies, race_get_dummies
from Procedure_Description_Codes import get_proc_code_descript_nums, get_diagnosis_description_nums
from CI_Methods import trends_table, proportion_NIS
from visuals_tables import characteristic_table
from Analysis import log_reg

NIS_16 = pl.scan_csv('NIS_PATH_2016_Here')
NIS_17 = pl.scan_csv('NIS_PATH_2017_Here')
NIS_18 = pl.scan_csv('NIS_PATH_2018_Here')
NIS_19 = pl.scan_csv('NIS_PATH_2019_Here')
NIS_20 = pl.scan_csv('NIS_PATH_2020_Here')
NIS_21 = pl.scan_csv('NIS_PATH_2021_Here')

NIS_Yrs = [NIS_16, NIS_17, NIS_18, NIS_19, NIS_20, NIS_21]\

#Choose ICD-10 CM or PCS codes to subset down to
subset_val = []
NIS_yrs = [NIS_16, NIS_17, NIS_18, NIS_19, NIS_20, NIS_21]

df = Subset_Procedure(NIS_yrs, subset_val)
# So no need to spend 1-3 minutes resubsetting each time
df.collect().write_csv('New csv file')


df = pd.read_csv('read new csv file')

#Diagnostic and procedure codes with description
df_pc = pd.read_csv("C:\\Users\\zacha\\Desktop\\Research_CSV_Files\\Procedure_Codes.csv")
df_diag = pd.read_csv("C:\\Users\\zacha\\Desktop\\Research_CSV_Files\\Diagnosis_Codes.csv")

#Get counts descriptions all procedure, diagnosis, and primary diagnosis codes
proc_code_counts = get_proc_code_descript_nums(df, df_pc)
diag_code_counts = get_diagnosis_description_nums(df, df_diag)
temp = df['I10_DX1'].value_counts(ascending=False).reset_index()
df_diag.rename(columns = {'CODE': 'I10_DX1'}, inplace= True)
temp = temp.merge(df_diag, how = 'left', on = 'I10_DX1')
print(temp)
print(diag_code_counts.head())

post_TA_AA = df.select(pl.len()).collect().item()

df = get_variables_DX(df, 'D63', '')

df = df.filter(pl.col('LOS') <= 50.0)
Post_los = df.select(pl.len()).collect().item()

#Get trends 
trends = trends_table()

#choose columns to keep
cols_to_keep = []

df = df[[cols_to_keep]]

df = race_get_dummies(df)
df = region_get_dummies(df)
df = Pay_1(df)


#Table 1 (characteristic table)
char_table = characteristic_table(df, 'HISTORY_BARIATRIC_SURGERY')
proportion_NIS(df, 'HISTORY_BARIATRIC_SURGERY')


#confidence intervals 


#logistic regression table
df.replace({2016: 0.0, 2017: 1.0, 2018: 2.0, 2019: 3.0, 2020: 4.0, 2021: 5.0}, inplace= True)

df = df[['MEDICARE', 'MEDICAID', 'PRIVATE_INSURANCE', 'SELF_PAY', 'PL_NCHS', 
'DIED', 'AGE', 'YEAR', 'FEMALE', 'ZIPINC_QRTL', 'NEW_ENGLAND',
'MID_ATLANTIC', 'EAST_NORTH_CENTRAL','WEST_NORTH_CENTRAL',
'EAST_SOUTH_CENTRAL', 'WEST_SOUTH_CENTRAL',
'MOUNTAIN','PACIFIC', 'BLACK','HISPANIC','ASIAN', 'WHITE','LOS']]

#Standardize variables, 1 std corresponds to OR associated risk
df['YEAR'] = (df['YEAR'] - df['YEAR'].mean()) / (df['YEAR'].std())
df['PL_NCHS'] = (df['PL_NCHS'] - df['PL_NCHS'].mean()) / (df['PL_NCHS'].std())
df['AGE'] = (df['AGE'] - df['AGE'].mean()) / (df['AGE'].std())
X = df.drop(['DIED', 'race', 'Region'], axis = 1)
y = df['LOS']

logreg = log_reg(X, y)

#Define methods table to make manuscript writing easy
methods_table = pd.DataFrame({
'Classification' : 
['Inclusions',
 'Exclusion',
 'Drop Missing',
 'Create Columns',
 'Char/Comp Tables',
 'Create Table',
 'Model',
 'Version Info'],
'Action': 
[ ' ', 
'Inclusion criteria',
'Exclusion criteria below',
'',
'', 
'',
'Logistic Regression Model Death Dependent (Year, PL_NCHS Standardized)',
'Software versions'
],
'N-Number': [
'',
'', 
'',
'',
'',
'',
'',
''] 
})


#convert dataframes to pandas and make excel files
with pd.ExcelWriter("name excel", engine="xlsxwriter") as writer:
    # Write dataframes to different sheets
    #Place holder
    temp.to_excel(writer, sheet_name="NAME", index=False)


