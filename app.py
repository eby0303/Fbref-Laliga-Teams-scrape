import streamlit as st
import pandas as pd
from scraper import run_all_scrapers
from db import client
import plotly.express as px

# Initialize connection to MongoDB
db = client['football']

def load_data(collection_name):
    """Load data from MongoDB collection"""
    collection = db[collection_name]
    data = list(collection.find({}))
    if data:
        return pd.DataFrame(data)
    return None

def main():
    st.title("La Liga Stats Dashboard")
    st.sidebar.title("Controls")

    # Add refresh button in sidebar
    if st.sidebar.button("Refresh Data"):
        with st.spinner("Scraping new data..."):
            scraped_data = run_all_scrapers()
            st.success("Data refreshed successfully!")
            st.rerun()

    # Create tabs for different stats
    tabs = [
        "Defensive Stats", "Possession Stats", "Pass Types Stats",
        "Miscellaneous Stats", "General Stats", "Goal Shot Stats",
        "Keeper Stats", "Passing Stats"
    ]
    selected_tab = st.tabs(tabs)

    # Defensive Stats Tab
    with selected_tab[0]:
        st.header("Defensive Statistics")
        defensive_df = load_data("laliga_defensive")
        if defensive_df is not None:
            st.dataframe(defensive_df)


    # Possession Stats Tab
    with selected_tab[1]:
        st.header("Possession Statistics")
        possession_df = load_data("laliga_possession")
        if possession_df is not None:
            st.dataframe(possession_df)


    # Pass Types Stats Tab
    with selected_tab[2]:
        st.header("Pass Types Statistics")
        passtypes_df = load_data("laliga_passtypes")
        if passtypes_df is not None:
            st.dataframe(passtypes_df)


    # Miscellaneous Stats Tab
    with selected_tab[3]:
        st.header("Miscellaneous Statistics")
        misc_df = load_data("laliga_misc")
        if misc_df is not None:
            st.dataframe(misc_df)

    # General Stats Tab
    with selected_tab[4]:
        st.header("General Statistics")
        stats_df = load_data("laliga_stats")
        if stats_df is not None:
            st.dataframe(stats_df)

    # Goal Shot Stats Tab
    with selected_tab[5]:
        st.header("Goal Shot Statistics")
        goalshot_df = load_data("laliga_goalshot")
        if goalshot_df is not None:
            st.dataframe(goalshot_df)

    # Keeper Stats Tab
    with selected_tab[6]:
        st.header("Keeper Statistics")
        keeper_df = load_data("laliga_keeper")
        if keeper_df is not None:
            st.dataframe(keeper_df)


    # Passing Stats Tab
    with selected_tab[7]:
        st.header("Passing Statistics")
        passing_df = load_data("laliga_passing")
        if passing_df is not None:
            st.dataframe(passing_df)


if __name__ == "__main__":
    main()