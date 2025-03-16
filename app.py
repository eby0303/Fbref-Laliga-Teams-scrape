import streamlit as st
import pandas as pd
from scraper import run_scraper
from db import client
import plotly.express as px

def load_data(year, team, stat_category):
    """Load data from the correct season's database and collection."""
    db = client[f"football_{year}"]  # ✅ Select the correct season database
    collection_name = f"{team}_{stat_category}"  # ✅ Example: "Barcelona_laliga_defensive"
    collection = db[collection_name]

    data = list(collection.find())
    if data:
        return pd.DataFrame(data)
    return None

def main():
    st.title("La Liga Stats Dashboard")
    st.sidebar.title("Controls")

    # Add user input fields
    selected_year = st.sidebar.text_input("Enter Season (e.g., 2023-24):", "2023-24")
    selected_team = st.sidebar.text_input("Enter Team (e.g., Barcelona):", "Barcelona")

    # Mapping tab names to scraper names
    collection_mapping = {
        "Defensive Stats": "laliga_defensive",
        "Possession Stats": "laliga_possession",
        "Pass Types Stats": "laliga_passtypes",
        "Miscellaneous Stats": "laliga_misc",
        "General Stats": "laliga_stats",
        "Goal Shot Stats": "laliga_goalshot",
        "Keeper Stats": "laliga_keeper",
        "Passing Stats": "laliga_passing"
    }

    selected_tab = st.sidebar.radio("Select Stats Category", list(collection_mapping.keys()))

    if st.sidebar.button("Refresh Data"):
        stat_category = collection_mapping[selected_tab]
        with st.spinner(f"Scraping {selected_tab} data for {selected_team} in {selected_year}..."):
            run_scraper(selected_year, selected_team, stat_category)  # ✅ Scrape only the selected stat
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
