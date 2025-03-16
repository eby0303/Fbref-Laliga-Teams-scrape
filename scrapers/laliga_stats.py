import sys
import os

# Add the parent directory (Football-Scrape) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.scraper_utils import retry_on_failure, validate_scrape, safe_read_html
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Dictionary of Squad IDs for teams
SQUAD_IDS = {
     "Real Madrid": "206d90db",
    "Barcelona": "206d90db",  # Replace with correct ID
    "Atletico Madrid": "db3b9613",
    "Valencia":"dcc91a7b",
    "Athletic Club":"2b390eca",
    "Rayo Vallecano":"98e8af82",
    "Valladolid":"17859612",
    "Girona":"9024a00a",
    "Villarreal":"2a8183b3",
    "Getafe":"7848bd64",
   "Osasuna":"03c57e2b",
    "Alaves": "8d6fd021",
    "Sevilla": "ad2be733",
   "Espanyol": "a8661628",
   "Real Sociedad":"e31d1cd9",
   "Celta Vigo" : "f25da7fb",
   "Las Palmas": "0049d422",
   "Mallorca":"2aa12281",
  "Real Betis": "fc536746",
  "Leganes" : "7c6f2c78"
}

@retry_on_failure(max_retries=3, delay=5)
def process_stats(year, team):
    """Process general statistics dynamically for any team and season."""
    logger.info(f"Starting general stats scraping for {team} in {year}")

    # Get Squad ID for the team
    if team not in SQUAD_IDS:
        raise ValueError(f"No squad ID found for team: {team}")

    squad_id = SQUAD_IDS[team]

    # Construct the URL dynamically
    url = f'https://fbref.com/en/squads/{squad_id}/{year}/matchlogs/c12/summary/{team.replace(" ", "-")}-Match-Logs-La-Liga'
    table_id = 'matchlogs_for'

    # Print URL for debugging
    print(f"🔍 Checking URL: {url}")
    print(f"🔍 Table ID: {table_id}")

    try:
        # Read the HTML table
        logger.info(f"Attempting to read HTML table for {team} in {year}")
        df_list = safe_read_html(url, table_id)

        if not df_list:
            raise ValueError(f"No tables found in the URL for {team} in {year}")

        df = df_list[0]
        logger.info(f"Successfully read HTML table for {team} in {year}")

        # Select relevant columns
        df = df.iloc[:, :-1]  # Remove last column if unnecessary

        # Remove the last row
        df = df.iloc[:-1]

        # Reset the index for a clean dataframe
        df.reset_index(drop=True, inplace=True)

        # Validate the scraping
        if not validate_scrape(df, __name__):
            raise ValueError(f"Scraping validation failed for {team} ({year})")

        return df

    except Exception as e:
        logger.error(f"Error in process_stats for {team} ({year}): {str(e)}")
        raise


