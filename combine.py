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
                dim_player.player_id
                , dim_player.player_name
                , facts_win_lose_kpi_weather.match_id
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
                , dim_match.match_id
                , dim_match.tourney_id
                , dim_match.match_num
                , dim_match.tourney_name
                , dim_match.tourney_date
                , dim_match.tourney_level
                , dim_match.winner_name
                , dim_match.loser_name
                , dim_match.score
                , dim_match.best_of
                , dim_match.round
                , dim_match.minutes 
                FROM dim_player 
                JOIN facts_win_lose_kpi_weather 
                ON dim_player.player_id = facts_win_lose_kpi_weather.player_id 
                JOIN dim_match 
                ON facts_win_lose_kpi_weather.match_id = dim_match.match_id
""")

data = tb.df()

# Page Setup
st.title('🎾 Tennis Analytics Dashboard')
tab1, tab2 = st.tabs(["Player Performance Across Different Grand Slam", "Weather Impact to Number of Aces"])

with tab1:
    # Page 1: Player Performance on Different Surfaces
    st.header("Player Performance on Different Surfaces")
    st.caption("This page shows the variation of player performance across different Grand Slam tournaments")

    # Dropdown to select player
    selected_player = st.selectbox("Select Player", data['player_name'].unique())

    # Split the page into two columns
    col1, col2 = st.columns(2)

    # Service Stats
    with col1:
        st.header("Number of Aces & Double Faults")
        # Select 1 player, 1 kpi, 1 surface
        tb2 = conn.execute(f"""
                                SELECT 
                                tourney_name AS Tournament
                                , AVG(ace) AS Ace
                                , AVG(df) AS 'Double Fault'
                                FROM tb
                                WHERE winner_name = ?
                                AND tourney_name IN ('Wimbledon', 'Roland Garros', 'Us Open', 'Australian Open') GROUP BY tourney_name;
                                """
                                , [selected_player])
        kpi_data = tb2.df()
        st.bar_chart(kpi_data, x="Tournament", y=["Ace", "Double Fault"], color=["#0000FF", "#FF0000"])

        st.header("Number of Service Games Played")
        # Select 1 player, 1 kpi, 1 surface
        tb9 = conn.execute(f"""
                              SELECT 
                               tourney_name AS Tournament
                               , AVG(SvGms) AS 'Service Games'
                               FROM tb
                               WHERE winner_name = ?
                               AND tourney_name IN ('Wimbledon', 'Roland Garros', 'Us Open', 'Australian Open') 
                               GROUP BY tourney_name;
                          """
                          , [selected_player])
        kpi8_data = tb9.df()
        st.bar_chart(kpi8_data, x="Tournament", y=["Service Games"], color=["#0000FF"])

    with col2:
        st.header("Serve Points Won Percentage")
        tb3 = conn.execute(f"""
                                SELECT 
                                AVG("1stWon") AS 'First Serve Points Won'
                                , AVG("2ndWon") AS 'Second Serve Points Won'
                                , tourney_name AS Tournament
                                FROM tb
                                WHERE winner_name = ? 
                                AND tourney_name IN ('Wimbledon', 'Roland Garros', 'Us Open', 'Australian Open') GROUP BY tourney_name;
                                """  
                                , [selected_player])
        kpi2_data = tb3.df()
        st.bar_chart(kpi2_data, x="Tournament", y=["First Serve Points Won", "Second Serve Points Won"], color=["#0000FF", "#FF0000"])
    

        st.header("Break Points Saved vs. Break Points Not Saved")
        tb4 = conn.execute(f""" 
                        SELECT 
                        tourney_name AS Tournament
                        , AVG(bPSaved) AS 'Break Points Saved'
                        , AVG(bPFaced) AS 'Break Points Faced'
                        , AVG(bPFaced - bPSaved) AS 'Break Points Not Saved'
                        FROM tb
                        WHERE winner_name = ?
                        AND tourney_name IN ('Wimbledon' , 'Roland Garros', 'Us Open', 'Australian Open') GROUP BY tourney_name;
                        """
                        , [selected_player])
        kpi3_data = tb4.df()
        st.bar_chart(kpi3_data, x="Tournament", y=["Break Points Saved", "Break Points Not Saved"], color=["#FF0000", "#0000FF"])

with tab2:
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
        tb5 = conn.execute(f"""
                                SELECT 
                                tourney_name AS Tournament
                                , ace AS Ace
                                , temperature AS Temperature
                                FROM tb
                                WHERE tourney_name = ?
                                """
                                , [selected_tourney])
        kpi4_data = tb5.df()
        st.scatter_chart(kpi4_data, x="Temperature", y=["Ace"], color=["#0000FF"])

        st.header("Impact of Humidity to Number of Aces")
        # Select 1 weather parameter and 1 kpi
        tb6 = conn.execute(f"""
                                SELECT 
                                tourney_name AS Tournament
                                , ace AS Ace
                                , humidity AS Humidity
                                FROM tb
                                WHERE tourney_name = ?
                                """
                                , [selected_tourney])
        kpi5_data = tb6.df()
        st.scatter_chart(kpi5_data, x="Humidity", y=["Ace"], color=["#0000FF"])


    with col2:
        st.header("Impact of Wind Speed to Number of Aces")
        tb7 = conn.execute(f"""
                                SELECT 
                                tourney_name AS Tournament
                                , ace AS Ace
                                , wind_speed AS "Wind Speed"
                                , temperature AS Temperature
                                FROM tb
                                WHERE tourney_name = ?
                                """
                                , [selected_tourney])
        kpi6_data = tb7.df()
        st.scatter_chart(kpi6_data, x="Wind Speed", y=["Ace"], color=["#0000FF"])

        st.header("Impact of Wind Direction to Number of Aces")
        # Select 1 weather parameter and 1 kpi
        tb8 = conn.execute(f"""
                                SELECT 
                                tourney_name AS Tournament
                                , ace AS Ace
                                , wind_direction AS "Wind Direction" 
                                FROM tb
                                WHERE tourney_name = ?
                                """
                                , [selected_tourney])
        kpi7_data = tb8.df()
        st.scatter_chart(kpi7_data, x="Wind Direction", y=["Ace"], color=["#0000FF"])

