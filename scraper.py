import importlib
import os
from db import update_data, check_if_scraping_needed
import logging

logger = logging.getLogger(__name__)

SCRAPER_FOLDER = "scrapers"

def run_scraper(year, team, stat_category):
    """Run a single scraper for the requested stat category."""
    try:
        if not check_if_scraping_needed(team, stat_category, year):
            logger.info(f"📊 Skipping {stat_category} - Recent data exists for {team} ({year})")
            return None

        module_name = f"{SCRAPER_FOLDER}.{stat_category}"  # Example: scrapers.laliga_defensive
        module = importlib.import_module(module_name)

        function_name = f"process_{stat_category.split('_')[1]}_stats"
        if stat_category == "laliga_stats":
            function_name = "process_stats"
        
        process_function = getattr(module, function_name)

        logger.info(f"🔄 Running {function_name}({year}, {team}) from {stat_category}...")
        data = process_function(year, team)  # Run the scraper

        if data is not None:
            update_data(data, year, team, stat_category)  # ✅ Store in MongoDB
            logger.info(f"✅ Successfully scraped {stat_category} for {team} ({year})")
        return data

    except Exception as e:
        logger.error(f"❌ Error running {stat_category}: {e}")
        return None
