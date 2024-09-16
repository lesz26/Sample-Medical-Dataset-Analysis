import pandas as pd
import re

#Returns all inputted ICD-10 with descriptions as excel file and pandas df
def get_description_ICD_10(list_codes: list[str], words: list[str]) -> pd.DataFrame:
    #cleaned csv files for PCS and CM codes
    df_ps = pd.read_csv('C:\\Users\\zacha\\Desktop\\Research_CSV_Files \
                        \\Procedure_Codes.csv')
    df_diag = pd.read_csv('C:\\Users\\zacha\\Desktop\\Research_CSV_Files \
                          \\Diagnosis_Codes.csv')
    df_description = pd.DataFrame()
    #look through entire list ICD-10 codes and append to df with description
    for i in range(len(list_codes)):
        if ((df_ps['CODE'].str.startswith(list_codes[i])).any()):
            temp = df_ps[df_ps['CODE'].str.startswith(list_codes[i])]
            df_ps['TYPE'] = 'PCS'
            df_description = pd.concat([df_description, temp], axis = 0)
        if ((df_diag['CODE'].str.startswith(list_codes[i])).any()):
            temp = df_diag[df_diag['CODE'].str.startswith(list_codes[i])]
            df_diag['TYPE'] = 'CM'
            df_description = pd.concat([df_description, temp], axis = 0)
    print(df_description.columns)
    df_ps['Description'] = df_ps['Description'].str.lower()
    df_diag['Description'] = df_diag['Description'].str.lower()
    for i in range(len(words)):
        if ((df_ps['Description'].str.contains(words[i])).any()):
                temp = df_ps[df_ps['Description'].str.contains(words[i])]
                df_ps['TYPE'] = 'PCS'
                df_description = pd.concat([df_description, temp], axis = 0)
        if ((df_diag['Description'].str.contains(words[i])).any()):
            temp = df_diag[df_diag['Description'].str.contains(words[i])]
            df_diag['TYPE'] = 'CM'
            df_description = pd.concat([df_description, temp], axis = 0)
    print(df_description)
    df_description.to_excel('Library_Codes.xlsx', index = False)
    return df_description
