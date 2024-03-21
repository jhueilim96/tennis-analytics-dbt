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
                , dim_player.first_name, dim_player.last_name, dim_player.country, dim_player.age, dim_player.height, dim_player.rank, dim_player.points, facts_win_lose_kpi.match_id, facts_win_lose_kpi.tourney_date, facts_win_lose_kpi.match_start_hour, facts_win_lose_kpi.is_win, facts_win_lose_kpi.ace, facts_win_lose_kpi.df, facts_win_lose_kpi.svpt, facts_win_lose_kpi."1stIn", facts_win_lose_kpi."1stWon", facts_win_lose_kpi."2ndWon", facts_win_lose_kpi.SvGms, facts_win_lose_kpi.bpSaved, facts_win_lose_kpi.bpFaced, dim_match.match_id, dim_match.tourney_id, dim_match.match_num, dim_match.tourney_name, dim_match.tourney_date, dim_match.tourney_level, dim_match.winner_name, dim_match.loser_name, dim_match.score, dim_match.best_of, dim_match.round, dim_match.minutes 
                FROM dim_player 
                JOIN facts_win_lose_kpi 
                ON dim_player.player_id = facts_win_lose_kpi.player_id 
                JOIN dim_match 
                ON facts_win_lose_kpi.match_id = dim_match.match_id
""")

data = tb.df()

# Page Setup
st.title('🎾 Tennis Analytics Dashboard')

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
                              , ANY_VALUE(ace) AS Ace
                              , ANY_VALUE(df) AS 'Double Fault'
                              FROM tb
                              WHERE winner_name = ?
                              AND tourney_name IN ('Wimbledon', 'Roland Garros', 'Us Open', 'Australian Open') GROUP BY tourney_name;
                              """
                              , [selected_player])
    kpi_data = tb2.df()
    st.bar_chart(kpi_data, x="Tournament", y=["Ace", "Double Fault"], color=["#0000FF", "#FF0000"])

with col2:
    st.header("Serve Points Won Percentage")
    tb3 = conn.execute(f"""
                              SELECT 
                              ANY_VALUE("1stWon") AS 'First Serve Points Won'
                              , ANY_VALUE("2ndWon") AS 'Second Serve Points Won'
                              , tourney_name AS Tournament
                              FROM tb
                              WHERE winner_name = ? 
                              AND tourney_name IN ('Wimbledon', 'Roland Garros', 'Us Open', 'Australian Open') GROUP BY tourney_name;
                              """  
                              , [selected_player])
    kpi2_data = tb3.df()
    st.bar_chart(kpi2_data, x="Tournament", y=["First Serve Points Won", "Second Serve Points Won"], color=["#0000FF", "#FF0000"])


st.header("Break Points Saved vs. Faced")
tb4 = conn.execute(f""" 
                   SELECT 
                   tourney_name AS Tournament
                   , ANY_VALUE(bPSaved) AS 'Break Points Saved'
                   , ANY_VALUE(bPFaced) AS 'Break Points Faced'
                   , SUM (bPSaved) AS 'Total Break Points Saved'
                   , SUM (bPFaced) AS 'Total Break Points Faced'
                   FROM tb
                   WHERE winner_name = ?
                   AND tourney_name IN ('Wimbledon' , 'Roland Garros', 'Us Open', 'Australian Open') GROUP BY tourney_name;
                   """
                   , [selected_player])
kpi3_data = tb4.df()
st.bar_chart(kpi3_data, x="Tournament", y=["Break Points Saved", "Break Points Faced"], color=["#FF0000", "#0000FF"])

st.header('Weather Analysis on Service Game')