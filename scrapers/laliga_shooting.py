import pandas as pd
from utils.scraper_utils import retry_on_failure, validate_scrape
import logging

logger = logging.getLogger(__name__)

@retry_on_failure(max_retries=3, delay=5)
def process_shooting_stats():
    """Process shooting statistics with error handling"""
    logger.info("🏃 Starting shooting stats scraping")
    
    url = 'https://fbref.com/en/squads/206d90db/2024-2025/matchlogs/c12/shooting/Barcelona-Match-Logs-La-Liga'
    table_id = 'matchlogs_for'

    try:
        # Read the HTML table
        logger.info("📊 Attempting to read HTML table")
        df_list = pd.read_html(url, attrs={'id': table_id})
        
        if not df_list:
            raise ValueError("No tables found in the URL")
            
        df = df_list[0]

        # Select columns up to 'np:G-xG'
        columns_to_keep = df.columns.get_loc(('Expected', 'np:G-xG')) + 1
        df = df.iloc[:, :columns_to_keep]

        # Remove the last row and reset index
        df = df.iloc[:-1]
        df.reset_index(drop=True, inplace=True)

        # Validate the scraping
        if not validate_scrape(df, __name__):
            raise ValueError("Scraping validation failed")

        return df

    except Exception as e:
        logger.error(f"❌ Error in process_shooting_stats: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        df = process_shooting_stats()
        print("✅ Scraping successful!")
        print(f"📊 DataFrame shape: {df.shape}")
        print("\n📋 First few rows:")
        print(df.head())
    except Exception as e:
        print(f"❌ Scraping failed: {str(e)}")


