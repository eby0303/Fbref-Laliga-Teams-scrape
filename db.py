from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)

def check_if_scraping_needed(team, stat_category, year, hours_threshold=24):
    """
    Check if scraping is needed based on last update time.
    Returns True if scraping is needed, False otherwise.
    """
    try:
        db = client[f"football_{year}"]  # ✅ Use season-specific database
        collection_name = f"{team}_{stat_category}"  # ✅ Example: "Barcelona_laliga_defensive"
        collection = db[collection_name]

        existing_data = collection.find_one({"team": team, "year": year})

        if not existing_data:
            logger.info(f"🆕 No data found for {team} ({year}) in {stat_category}. Scraping needed.")
            return True

        last_update = existing_data.get('last_updated', datetime.min)
        if isinstance(last_update, str):
            last_update = datetime.fromisoformat(last_update.replace('Z', '+00:00'))

        if datetime.now() - last_update > timedelta(hours=hours_threshold):
            logger.info(f"⏳ Data for {team} ({year}) in {stat_category} is outdated. Scraping needed.")
            return True

        logger.info(f"✅ Recent data exists for {team} ({year}) in {stat_category}. Skipping scrape.")
        return False

    except Exception as e:
        logger.error(f"❌ Error checking {team}_{stat_category}: {e}")
        return True  # Assume scraping is needed if there's an error

def update_data(df, year, team, stat_category):
    """Update MongoDB with new scraped data."""
    try:
        db = client[f"football_{year}"]  # ✅ Store in season-specific database
        collection_name = f"{team}_{stat_category}"  # ✅ Store each stat in a unique collection
        collection = db[collection_name]

        if df is not None and not df.empty:
            current_time = datetime.now()
            df["last_updated"] = current_time
            df["team"] = team
            df["year"] = year
            df["stat"] = stat_category

            # Convert DataFrame to records
            data_dict = df.to_dict(orient="records")

            for record in data_dict:
                try:
                    date = record.get("Date", "")
                    if date:
                        record["_id"] = f"{team}_{year}_{stat_category}_{date}"

                    # Insert or update the record
                    collection.update_one(
                        {"_id": record["_id"]},
                        {"$set": record},
                        upsert=True
                    )

                except Exception as e:
                    logger.error(f"❌ Error updating record in {collection_name}: {e}")

            logger.info(f"✅ Successfully updated {collection_name} with {len(data_dict)} records")

        else:
            logger.warning(f"⚠️ Skipping {collection_name} update - No valid data")

    except Exception as e:
        logger.error(f"❌ Error updating database: {e}")
        raise
