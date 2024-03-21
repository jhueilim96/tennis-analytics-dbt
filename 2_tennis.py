import streamlit as st
import pandas as pd
import altair as alt
import duckdb
from pathlib import Path

# Path to the DuckDB file
db_file = "C:/users/azuraaziz.azizahmad/tennis-analytics/ta_dbt/ta.duckdb"
conn = duckdb.connect(db_file)

# Fetching data from the database
tb = conn.sql("""
   SELECT 
                facts_win_lose_kpi_weather.match_id
                , facts_win_lose_kpi_weather.player_id
                , facts_win_lose_kpi_weather.match_date
                , facts_win_lose_kpi_weather.match_start_hour
                , facts_win_lose_kpi_weather.is_win
                , facts_win_lose_kpi_weather.ace
                , facts_win_lose_kpi_weather.df
                , facts_win_lose_kpi_weather.svpt
                , facts_win_lose_kpi_weather."1stIn"
                , facts_win_lose_kpi_weather."1stWon"
                , facts_win_lose_kpi_weather."2ndWon"
                , facts_win_lose_kpi_weather.SvGms
                , facts_win_lose_kpi_weather.bpSaved
                , facts_win_lose_kpi_weather.bpFaced
                , facts_win_lose_kpi_weather.temperature
                , facts_win_lose_kpi_weather.humidity
                , facts_win_lose_kpi_weather.precipitation
                , facts_win_lose_kpi_weather.cloud_cover
                , facts_win_lose_kpi_weather.wind_speed
                , facts_win_lose_kpi_weather.wind_direction
                , facts_win_lose_kpi_weather.soil_temperature
                , dim_match.tourney_name 
                FROM facts_win_lose_kpi_weather
                JOIN dim_player
                ON facts_win_lose_kpi_weather.player_id = dim_player.player_id 
                JOIN dim_match 
                ON facts_win_lose_kpi_weather.match_id = dim_match.match_id
""")

data = tb.df()

# Page Setup
st.title('🎾 Tennis Analytics Dashboard')

# Page 1: Weather Impact 
st.header("Impact of Weather on Tennis Service Game ")
st.caption("This page shows the impact of atmospheric temperature, humidity, precipitation, cloud coverage, wind speed, soil temperature, wind direction on service KPI")

# Dropdown to select player
selected_tourney= st.selectbox("Select Tournament", data['tourney_name'].unique())

# Split the page into two columns
col1, col2 = st.columns(2)

# Service Stats
with col1:
    st.header("Impact of Temperature to Number of Aces")
    # Select 1 weather parameter and 1 kpi
    tb2 = conn.execute(f"""
                              SELECT 
                              tourney_name AS Tournament
                              , ace AS Ace
                              , temperature AS Temperature
                              FROM tb
                              WHERE tourney_name = ?
                              """
                              , [selected_tourney])
    kpi_data = tb2.df()
    st.scatter_chart(kpi_data, x="Temperature", y=["Ace"], color=["#0000FF"])

    st.header("Impact of Humidity to Number of Aces")
    # Select 1 weather parameter and 1 kpi
    tb4 = conn.execute(f"""
                              SELECT 
                              tourney_name AS Tournament
                              , ace AS Ace
                              , humidity AS Humidity
                              FROM tb
                              WHERE tourney_name = ?
                              """
                              , [selected_tourney])
    kpi3_data = tb4.df()
    st.scatter_chart(kpi3_data, x="Humidity", y=["Ace"], color=["#0000FF"])


with col2:
    st.header("Impact of Wind Speed to Number of Aces")
    tb3 = conn.execute(f"""
                              SELECT 
                              tourney_name AS Tournament
                              , ace AS Ace
                              , wind_speed AS "Wind Speed"
                              , temperature AS Temperature
                              FROM tb
                              WHERE tourney_name = ?
                              """
                              , [selected_tourney])
    kpi2_data = tb3.df()
    st.scatter_chart(kpi2_data, x="Wind Speed", y=["Ace"], color=["#0000FF"])

    st.header("Impact of Wind Direction to Number of Aces")
    # Select 1 weather parameter and 1 kpi
    tb5 = conn.execute(f"""
                              SELECT 
                              tourney_name AS Tournament
                              , ace AS Ace
                              , wind_direction AS "Wind Direction" 
                              FROM tb
                              WHERE tourney_name = ?
                              """
                              , [selected_tourney])
    kpi4_data = tb5.df()
    st.scatter_chart(kpi4_data, x="Wind Direction", y=["Ace"], color=["#0000FF"])
