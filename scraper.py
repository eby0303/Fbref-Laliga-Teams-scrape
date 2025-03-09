import importlib
import os
from db import update_data, check_if_scraping_needed, get_collection_stats, view_collection_data
import logging
import time

logger = logging.getLogger(__name__)

# Path to the scrapers folder
SCRAPER_FOLDER = "scrapers"

def run_single_scraper(scraper_name):
    """Run a single scraper with proper error handling"""
    try:
        if not check_if_scraping_needed(scraper_name):
            logger.info(f"📊 Skipping {scraper_name} - Recent data exists")
            return None, scraper_name

        # Dynamically import the module
        module = importlib.import_module(f"{SCRAPER_FOLDER}.{scraper_name}")
        
        # Dynamically call the function
        function_name = f"process_{scraper_name.split('_')[1]}_stats"
        if scraper_name == "laliga_stats":
            function_name = "process_stats"
        
        process_function = getattr(module, function_name)
        
        # Run the scraping function
        logger.info(f"🔄 Running {function_name} from {scraper_name}...")
        data = process_function()
        logger.info(f"✅ Successfully scraped {scraper_name}")
        
        return data, scraper_name
        
    except Exception as e:
        logger.error(f"❌ Error running {scraper_name}: {e}")
        return None, scraper_name

def run_all_scrapers():
    """Run all scrapers sequentially"""
    scraper_files = [
        f.replace(".py", "") for f in os.listdir(SCRAPER_FOLDER) 
        if f.endswith(".py") and f != "__init__.py"
    ]

    all_data = {}

    for scraper_name in scraper_files:
        data, name = run_single_scraper(scraper_name)
        if data is not None:
            all_data[name] = data

    return all_data

if __name__ == "__main__":
    logger.info("🚀 Starting central scraper...")
    start_time = time.time()
    
    try:
        scraped_data = run_all_scrapers()
        
        if scraped_data:
            logger.info("📤 Sending data to database...")
            update_data(scraped_data)
            
            # Verify data was saved
            logger.info("\n📊 Checking saved data:")
            stats = get_collection_stats()
            for collection, data in stats.items():
                logger.info(f"\n{collection}:")
                logger.info(f"  Documents: {data['document_count']}")
                logger.info(f"  Last Updated: {data['last_updated']}")
            
            # Show sample of saved data
            df = view_collection_data(collection, limit=3)
            if df is not None and not df.empty:
                logger.info("\n  Latest saved records:")
                logger.info(f"{df.head().to_string()}")
        else:
            logger.info("ℹ️ No new data to update")
            
    except Exception as e:
        logger.error(f"❌ Scraping process failed: {str(e)}")
    finally:
        end_time = time.time()
        logger.info(f"⏱️ Total execution time: {end_time - start_time:.2f} seconds")