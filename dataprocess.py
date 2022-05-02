import pandas as pd
import streamlit as st


# function to preprocess the data file and remove redundant data based on the week of the date provided in file.
@st.cache()
def pre_process(data):
    countyColumns = data[['countyFIPS', 'County Name']]
    week_df = data.drop(['countyFIPS', 'County Name', 'State', 'StateFIPS'], axis=1)
    week_df = week_df.diff(axis=1)
    week_df = week_df.T.reset_index()
    week_df['week'] = week_df['index']
    week_df = week_df.drop(columns='index')
    week_df['week'] = week_df['week'].astype('datetime64[ns]')
# find start and end date of the file containing full weeks only
    start = week_df[week_df['week'].dt.dayofweek == 6].first_valid_index()
    end = week_df[week_df['week'].dt.dayofweek == 5].last_valid_index()
# slice dataframe to only consider full weeks
    week_df = week_df[start:end + 1]
    grouped = week_df.resample('w-sun', label='left', closed='left', on='week').sum()
    table = pd.merge(countyColumns, grouped.T, left_index=True, right_index=True)
    return table


# function to calculate rate for cases per 100000
@st.cache()
def rate(confirmed_data, population):
    df = pd.merge(confirmed_data, population, left_on=['countyFIPS'], right_on=['countyFIPS'])
    df['countyFIPS'] = df['countyFIPS'].apply(lambda x: '0' + x if len(x) == 4 else x)
    county = df[['countyFIPS','County Name']]
    finalTable = df.drop(['countyFIPS','County Name'], axis=1).apply(lambda x:( x / df['population']) * 100000)
    finalTable = finalTable.drop(['population'], axis=1)
    finalTable.columns = pd.to_datetime(finalTable.columns, utc=True).date
    finalTable.columns = finalTable.columns.astype(str)
    columns = finalTable.columns.values.tolist()
    final_df = pd.merge(county, finalTable, left_index=True, right_index=True)
    final_df = final_df.drop(final_df[final_df['countyFIPS'] == '0'].index)
    return final_df, columns
