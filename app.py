import streamlit as st
import pandas as pd
from scraper import run_scraper
from db import client
import plotly.express as px

def load_data(year, team, stat_category):
    """Load data from the correct season's database and collection."""
    db_name = f"football_{year}"
    collection_name = f"{team}_{stat_category}_{year}"
    db = client[db_name]  
    collection = db[collection_name]

    data = list(collection.find())
    if data:
        # Convert ObjectId to string for display
        for record in data:
            record['_id'] = str(record['_id'])
        return pd.DataFrame(data)
    return None

def main():
    st.title("La Liga Scraping Dashboard")
    st.sidebar.title("Select Fields")

    # Add user input fields
    selected_year = st.sidebar.text_input("Enter Season (e.g., 2023-2024):", "2023-2024")
    selected_team = st.sidebar.text_input("Enter Team (e.g., Barcelona):", "Barcelona")

    # Mapping tab names to scraper names
    collection_mapping = {
        "Defensive Stats": "laliga_defensive",
        "Possession Stats": "laliga_possession",
        "Pass Types Stats": "laliga_passtypes",
        "Miscellaneous Stats": "laliga_misc",
        "Schedule Stats": "laliga_stats",
        "Goal Shot Stats": "laliga_goalshot",
        "Keeper Stats": "laliga_keeper",
        "Passing Stats": "laliga_passing",
        "Shooting Stats": "laliga_shooting"
    }

    selected_tab = st.sidebar.radio("Select Stats Category", list(collection_mapping.keys()))

    if st.sidebar.button("Scrape Data"):
        stat_category = collection_mapping[selected_tab]
        with st.spinner(f"Scraping {selected_tab} data for {selected_team} in {selected_year}..."):
            run_scraper(selected_year, selected_team, stat_category, selected_year)
            st.success(f"Data for {selected_team} ({selected_year}) updated successfully!")
            st.rerun()

    # Fetch and display data from MongoDB
    st.header(selected_tab)
    stat_category = collection_mapping[selected_tab]
    df = load_data(selected_year, selected_team, stat_category)

    if df is not None:
        st.dataframe(df)
    else:
        st.warning(f"No data found for {selected_team} in {selected_year} for {selected_tab}.")

if __name__ == "__main__":
    main()
