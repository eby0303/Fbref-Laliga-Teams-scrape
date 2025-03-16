import importlib
import os
from db import update_data, check_if_scraping_needed


SCRAPER_FOLDER = "scrapers"
def run_scraper(year, team, stat_category, season):
    """Run a single scraper for the requested stat category."""
    try:
        if not check_if_scraping_needed(team, stat_category, year, season):
            print(f"📊 Skipping {stat_category} - Recent data exists for {team} ({year})")
            return None

        module_name = f"{SCRAPER_FOLDER}.{stat_category}"  
        module = importlib.import_module(module_name)

        function_name = f"process_{stat_category.split('_')[1]}_stats"
        if stat_category == "laliga_stats":
            function_name = "process_stats"
        
        process_function = getattr(module, function_name)

        print(f"🔄 Running {function_name}({year}, {team}) from {stat_category}...")
        data = process_function(year, team)  # Run the scraper

        # Debug statement to log the fetched data
        print(f"Fetched data for {team}: {data}")

        if data is not None:
            update_data(data, year, team, stat_category, season)  # Store in MongoDB
            print(f"✅ Successfully scraped {stat_category} for {team} ({year})")
        return data

    except Exception as e:
        print(f"❌ Error running {stat_category}: {e}")
        return None