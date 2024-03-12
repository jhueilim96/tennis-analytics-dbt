import streamlit as st
import pandas as pd
import altair as alt
import duckdb
from pathlib import Path

# Function to execute SQL queries
def execute_query(query: str, db_file: str, return_type: str = "df"):
    with duckdb.connect(db_file, read_only=True) as con:
        if return_type == "df":
            return con.execute(query).df()
        elif return_type == "arrow":
            return con.execute(query).arrow()
        elif return_type == "list":
            return con.execute(query).fetchall()

# Path to the DuckDB file
db_file = "C:/users/azuraaziz.azizahmad/tennis-analytics/ta_dbt/ta.duckdb"

# Name of the table
destination_table_name = "raw_atp_matches"

# Fetching data from the database
data = execute_query(f"SELECT * FROM {destination_table_name}", db_file, return_type="df")

# Page Setup
st.title('🎾 Tennis Analytics Dashboard')

# Page 1: Player Performance on Different Surfaces
st.header("Player Performance on Different Surfaces")
st.caption("This page shows the variation of player performance across different Grand Slam tournaments")

# Dropdown to select player
selected_player = st.selectbox("Select Player", data['winner_name'].unique())

# Split the page into two columns
col1, col2 = st.columns(2)

# Service Stats
with col1:
    st.header("Number of Aces & Double Faults")
    # Select 1 player, 1 kpi, 1 surface
    kpi_data = execute_query(f"SELECT tourney_name, ANY_VALUE(w_ace) AS w_ace, ANY_VALUE(w_df) AS w_df FROM {destination_table_name} WHERE winner_name = '{selected_player}' AND tourney_name IN ('Wimbledon', 'Roland Garros', 'Us Open', 'Australian Open') GROUP BY tourney_name;", db_file, return_type="df")

    # Show KPI data
    st.write(kpi_data)

    # Melt the kpi_data DataFrame into a long format
    kpi_data_melted = kpi_data.melt(id_vars='tourney_name', var_name='Statistic', value_name='Value')

    # Map column names to desired labels
    column_labels = {'w_ace': 'Aces', 'w_df': 'Double Faults'}
    kpi_data_melted['Statistic'] = kpi_data_melted['Statistic'].map(column_labels)

    # Create a DataFrame in the desired format
    chart_data = pd.DataFrame({
        'Tournament': kpi_data_melted['tourney_name'],
        'Stats': kpi_data_melted['Value'],
        'Legend': kpi_data_melted['Statistic']
    })

    # Plot the data using st.bar_chart()
    st.bar_chart(chart_data, x='Tournament', y='Stats', color='Legend')

# Return Stats
with col2:
    st.header("Serve Points Distribution")

# Select 1 player, 1 kpi, 1 surface
    kpi2_data = execute_query(f"SELECT tourney_name, ANY_VALUE(w_1stWon) AS w_1stWon, ANY_VALUE(w_2ndWon) AS w_2ndWon FROM {destination_table_name} WHERE winner_name = '{selected_player}' AND tourney_name IN ('Wimbledon', 'Roland Garros', 'Us Open', 'Australian Open') GROUP BY tourney_name;", db_file, return_type="df")

    # Show KPI data
    st.write(kpi2_data)

    # Melt the kpi_data DataFrame into a long format
    kpi2_data_melted = kpi2_data.melt(id_vars='tourney_name', var_name='Statistic', value_name='Value')

    # Map column names to desired labels
    column_labels = {'w_1stWon': '1st Serves Won', 'w_2ndWon': '2nd Serves Won'}
    kpi2_data_melted['Statistic'] = kpi2_data_melted['Statistic'].map(column_labels)

    # Create a DataFrame in the desired format
    chart_data = pd.DataFrame({
        'Tournament': kpi2_data_melted['tourney_name'],
        'Stats': kpi2_data_melted['Value'],
        'Legend': kpi2_data_melted['Statistic']
    })

    # Plot the data using st.bar_chart()
    st.bar_chart(chart_data, x='Tournament', y='Stats', color='Legend')


# Select 1 player, 1 kpi, 1 surface
kpi3_data = execute_query(f"SELECT tourney_name, w_1stIn, w_svpt FROM {destination_table_name} WHERE winner_name = '{selected_player}' AND tourney_name IN ('Wimbledon', 'Roland Garros', 'Us Open', 'Australian Open')", db_file, return_type="df")
kpi3_data['First Serve Percentage'] = (kpi3_data['w_1stIn'] / kpi3_data['w_svpt']) * 100

# Plot the data using streamlit line_chart()
st.header("First Serve Percentage Over Matches")
st.line_chart(kpi3_data.set_index('tourney_name')['First Serve Percentage'])