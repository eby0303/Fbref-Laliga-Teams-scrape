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
    tabs = ["Defensive Stats", "Possession Stats", "Pass Types Stats"]
    selected_tab = st.tabs(tabs)

    # Defensive Stats Tab
    with selected_tab[0]:
        st.header("Defensive Statistics")
        defensive_df = load_data("laliga_defensive")
        if defensive_df is not None:
            st.dataframe(defensive_df)
            
            # Example visualization
            if 'Tkl' in defensive_df.columns:
                fig = px.bar(defensive_df, x='Date', y='Tkl', title='Tackles per Game')
                st.plotly_chart(fig)

    # Possession Stats Tab
    with selected_tab[1]:
        st.header("Possession Statistics")
        possession_df = load_data("laliga_possession")
        if possession_df is not None:
            st.dataframe(possession_df)
            
            # Example visualization
            if 'Poss' in possession_df.columns:
                fig = px.line(possession_df, x='Date', y='Poss', title='Possession % per Game')
                st.plotly_chart(fig)

    # Pass Types Stats Tab
    with selected_tab[2]:
        st.header("Pass Types Statistics")
        passtypes_df = load_data("laliga_passtypes")
        if passtypes_df is not None:
            st.dataframe(passtypes_df)
            
            # Example visualization for pass types
            if 'Cmp' in passtypes_df.columns:
                fig = px.scatter(passtypes_df, x='Date', y='Cmp', title='Completed Passes per Game')
                st.plotly_chart(fig)

if __name__ == "__main__":
    main() 