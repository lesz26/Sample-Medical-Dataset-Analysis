import pandas as pd
import matplotlib.pyplot as plt
import math
import polars as pl

#subset on 2 ICD-10 procedure codes to lazy df, change for your use case
def Subset_Procedure(NIS_Yrs: list[pl.DataFrame.lazy], array_codes: list[str]) -> pl.DataFrame.lazy:
    df = pl.DataFrame().lazy()
    condition = pl.col(columns_to_filter).str.starts_with(array_codes[0]),
    pl.col(columns_to_filter).str.starts_with(array_codes[1])
    columns_to_filter = ['I10_PR1', 'I10_PR2', 'I10_PR3', 'I10_PR4', 'I10_PR5',
                         'I10_PR6', 'I10_PR7', 'I10_PR8', 'I10_PR9', 'I10_PR10',
                         'I10_PR11', 'I10_PR12', 'I10_PR13', 'I10_PR14', 'I10_PR15']
    #To get each year
    for i in range(0,len(NIS_Yrs)):
        Filtered_df = NIS_Yrs[i].filter(pl.any_horizontal(condition))
        df = pl.concat([df, Filtered_df], how= 'diagonal_relaxed')
    print(df.select(pl.len()).collect().item())
    return df

#subset on two ICD-10-CM diagnosis codes, change for your own use case
def Subset_Diagnosis(NIS_Yrs: list[pl.DataFrame.lazy], array_codes: list[str]) -> pl.DataFrame.lazy:
    df = pl.DataFrame().lazy()
    condition = pl.col(columns_to_filter).str.starts_with(array_codes[0]), \
                pl.col(columns_to_filter).str.starts_with(array_codes[1])           
    #To get each year
    for i in range(0,len(NIS_Yrs)):
        columns_to_filter = ['I10_DX1', 'I10_DX2', 'I10_DX3', 'I10_DX4', 'I10_DX5', 
                             'I10_DX6', 'I10_DX7', 'I10_DX8', 'I10_DX9', 'I10_DX10',
                             'I10_DX11', 'I10_DX12', 'I10_DX13', 'I10_DX14', 'I10_DX15',
                             'I10_DX16', 'I10_DX17', 'I10_DX18', 'I10_DX19', 'I10_DX20', 
                             'I10_DX21', 'I10_DX22', 'I10_DX23', 'I10_DX24', 'I10_DX25',
                             'I10_DX26', 'I10_DX27', 'I10_DX28', 'I10_DX29', 'I10_DX30']
        #Rust iterator chain to get correct subset columns
        Filtered_df = NIS_Yrs[i].filter(pl.any_horizontal(condition))
        df = pl.concat([df, Filtered_df], how= 'diagonal_relaxed')
    print(df.select(pl.len()).collect().item())
    return df  

    