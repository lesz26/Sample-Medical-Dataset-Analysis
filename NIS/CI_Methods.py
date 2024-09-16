import pandas as pd
import polars as pl
import math

#Returns a weighted trends table from NIS subset csv
def trends_table(column_name: str, operation_name: str, df: pl.DataFrame.lazy) -> pd.DataFrame:
    year_arr = [2016, 2017, 2018, 2019, 2020, 2021]
    return_df = pd.DataFrame()
    #each year, custom table
    for i in range(len(year_arr)):
        temp = df.filter(pl.col('YEAR') == year_arr[i])
        len_df = temp.select(pl.len()).collect().item()
        count = int((temp.select(pl.col(column_name)).sum().collect().item()) * 5)
        pct = round((count / len_df) / 5 * 100, 2)
        temp_df = pd.DataFrame({'Year': [year_arr[i]], 'Weighted ' + operation_name: [str(count) + ' (N=' + str(pct) +  '%)']})
        return_df = pd.concat([return_df, temp_df], axis = 0)
    return return_df

#Trends table for each year NASS, handling discharge weight as appropriate
def trends_table_NASS(column_name: str, operation_name: str, df: pl.DataFrame.lazy ) -> pd.DataFrame:
    year_arr = [2016, 2017, 2018, 2019, 2020, 2021]
    return_df = pd.DataFrame()
    for i in range(0,6):
        temp = df.filter(pl.col('year') == year_arr[i])
        full_size = temp.select(pl.col('discwt')).mean().collect().item() * temp.select(pl.len()).collect().item()
        print(full_size)
        temp = temp.filter(pl.col(column_name) == 1.0)
        w_mean = temp.select(pl.col('discwt')).mean().collect().item()
        statistic = w_mean * (temp.select(pl.len()).collect().item())
        percent = round(100 * (statistic / full_size), 2) 
        temp_df = pd.DataFrame({'Year': [year_arr[i]], column_name + 'Weighted_count': [str(math.floor(statistic)) + ' (' + str(percent) + '%)']})
        return_df = pd.concat([return_df, temp_df], axis = 0)
    return return_df

#Obtain CI error from point estimate as proportion for value within NIS
def proportion_NIS(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    year_arr = [2016, 2017, 2018, 2019, 2020, 2021]
    con_975 = []
    con_025 = []
    for i in range(len(year_arr)):
        temp = df[df['YEAR'] == year_arr[i]]
        z95 = 1.6449
        SE =100 *  (1.649 * 2 * (temp[column_name].std() / (math.sqrt(len(temp)))))

        con_975.append(SE)
        print(con_975)
    return con_975
