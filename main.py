"""
 Assignment 2: Question 1, 2,3,4,5,6
 Name: Lakshmi Biradar
 Redid: 825975651
"""
#path for the files
confirmed_cases_path = 'assignment2Data/covid_confirmed_usafacts.csv'
population_info_path = 'assignment2Data/covid_county_population_usafacts.csv'
death_cases_path = 'assignment2Data/covid_deaths_usafacts.csv'

import pandas as pd
from urllib.request import urlopen
import json
import streamlit as st
import plotly.express as px
from dataprocess import pre_process, rate

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
confirmed_df = pd.read_csv(confirmed_cases_path, dtype={'countyFIPS': str})
DeathCases_df = pd.read_csv(death_cases_path, dtype={'countyFIPS': str})
population_df = pd.read_csv(population_info_path, dtype={'countyFIPS': str}).drop(
    ['County Name', 'State'], axis=1)

# Pre-process data to group by week removing unwanted and redundant data for confirmed cases and Death cases.
# call function pre_process  for Death cases and Confirmed cases to club data and get only week columns

Confirm_df = pre_process(confirmed_df)
Death_df = pre_process(DeathCases_df)

#  drop unwanted columns
Confirm = Confirm_df.drop(['countyFIPS', 'County Name'], axis=1).sum(axis=0).reset_index(name='Total Cases')
Confirm.set_index(['index'], inplace=True)
Death = Death_df.drop(['countyFIPS', 'County Name'], axis=1).sum(axis=0).reset_index(name='Total Deaths')
Death.set_index(['index'], inplace=True)
# plot
st.header("Confirmed Cases")
st.line_chart(Confirm, use_container_width=True)
st.header("Confirmed Deaths")
st.line_chart(Death, use_container_width=True)

# call rate function to calculate rate per 100000 population for each county
confirmed_cases_df, column = rate(Confirm_df, population_df)
death_cases_df, column2 = rate(Death_df, population_df)
st.header("Confirmed cases, Death Cases  rate")
week = st.select_slider('select Week', options=column)

# reserve spot to update both the figure
plot_spot = st.empty()
if st.button('Play Animation'):
    for col in column:
        fig_confirmCases = px.choropleth(confirmed_cases_df, geojson=counties, locations='countyFIPS', color=col,
                                         color_continuous_scale="reds",
                                         range_color=(0, 5745),
                                         scope="usa",
                                         labels={'rate': 'Case rate'},
                                         hover_name='County Name',
                                         title='<b>Confirmed Cases rate per week animation</b> <br> showing data for week ' +col,
                                         )
        fig_deathCases = px.choropleth(death_cases_df, geojson=counties, locations='countyFIPS', color=col,
                                       color_continuous_scale="reds",
                                       range_color=(0, 100),
                                       scope="usa",
                                       labels={'rate': 'Case rate'},
                                       hover_name='County Name',
                                       title='<b>Death Cases rate per week animation</b> <br> showing data for week ' +col
                                       )
        with plot_spot.container():
            st.plotly_chart(fig_confirmCases, use_container_width=True)
            st.plotly_chart(fig_deathCases, use_container_width=True)

else:
    fig_confirmCases = px.choropleth(confirmed_cases_df, geojson=counties, locations='countyFIPS', color=week,
                                     color_continuous_scale="Reds",
                                     range_color=(0, 5745),
                                     scope="usa",
                                     labels={'rate': 'Case rate'},
                                     hover_name='County Name',
                                     title='<b>Confirmed Cases rate per week </b> <br> showing data for week ' +week,
                                     )
    fig_deathCases = px.choropleth(death_cases_df, geojson=counties, locations='countyFIPS', color=week,
                                   color_continuous_scale="Reds",
                                   range_color=(0, 100),
                                   scope="usa",
                                   labels={'rate': 'Case rate'},
                                   hover_name='County Name',
                                   title='<b>Death Cases rate per week </b> <br> showing data for week ' +week,
                                   )
    with plot_spot.container():
        st.plotly_chart(fig_confirmCases, use_container_width=True)
        st.plotly_chart(fig_deathCases, use_container_width=True)
# plot rate map


