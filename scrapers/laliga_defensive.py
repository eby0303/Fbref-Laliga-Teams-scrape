import pandas as pd
from utils.scraper_utils import retry_on_failure, validate_scrape, safe_read_html
import logging

logger = logging.getLogger(__name__)

@retry_on_failure(max_retries=3, delay=5)
def process_defensive_stats():
    """Process defensive statistics with error handling"""
    logger.info("🏃 Starting defensive stats scraping")
    
    url = 'https://fbref.com/en/squads/206d90db/2024-2025/matchlogs/c12/defense/Barcelona-Match-Logs-La-Liga'
    table_id = 'matchlogs_for'

    try:
        # Read the HTML table using the safe reader
        logger.info("📊 Attempting to read HTML table")
        df_list = safe_read_html(url, table_id)
        
        if not df_list:
            raise ValueError("No tables found in the URL")
            
        df = df_list[0]
        logger.info("✅ Successfully read HTML table")

        # Select columns up to 'Err'
        columns_to_keep = df.columns.get_loc(('Unnamed: 24_level_0', 'Err')) + 1 
        df = df.iloc[:, :columns_to_keep]  

        # Remove the last row
        df = df.iloc[:-1]  

        # Reset the index for a clean dataframe
        df.reset_index(drop=True, inplace=True)

        # Validate the scraping
        if not validate_scrape(df, __name__):
            raise ValueError("Scraping validation failed")

        return df

    except Exception as e:
        logger.error(f"❌ Error in process_defensive_stats: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        df = process_defensive_stats()
        print("✅ Scraping successful!")
        print(f"📊 DataFrame shape: {df.shape}")
        print("\n📋 First few rows:")
        print(df.head())
    except Exception as e:
        print(f"❌ Scraping failed: {str(e)}")
