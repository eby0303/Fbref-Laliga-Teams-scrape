from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd


load_dotenv()

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)

def get_season_db(season):
    db_name = f"football_{season}"
    return client[db_name]

def check_if_scraping_needed(team, stat_category, year, season, hours_threshold=24):
    db = get_season_db(season)
    collection_name = f"{team}_{stat_category}_{year}"
    collection = db[collection_name]
    
    if collection.count_documents({}) == 0:
        print(f"Collection {collection_name} is empty. Scraping needed.")
        return True
        
    latest_doc = collection.find_one(
        sort=[('last_updated', -1)]
    )
    
    if not latest_doc:
        return True
        
    current_time = datetime.now()
    last_update = latest_doc.get('last_updated', datetime.min)
    
    if isinstance(last_update, str):
        last_update = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
        
    time_difference = current_time - last_update
    
    if time_difference > timedelta(hours=hours_threshold):
        print(f"Data in {collection_name} is older than {hours_threshold} hours. Scraping needed.")
        return True
        
    print(f"Recent data exists in {collection_name}. Skipping scrape.")
    return False

def verify_database_connection():
    client.admin.command('ping')
    print("✅ MongoDB connection successful")
    
    collections = [
        'laliga_defensive',
        'laliga_possession',
        'laliga_passtypes',
        'laliga_stats',
        'laliga_keeper',
        'laliga_passing',
        'laliga_goalshot',
        'laliga_misc',
        'laliga_shooting'
    ]
    
    season = "2023-2024"  # Example 
    db = get_season_db(season)
    for collection_name in collections:
        collection = db[collection_name]
        collection.create_index('last_updated')
        print(f"✅ Verified collection: {collection_name}")
        
    return True

def update_data(data, year, team, stat_category, season):
    db = get_season_db(season)
    collection_name = f"{team}_{stat_category}_{year}"
    collection = db[collection_name]
    
    if data is not None and not data.empty:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] 
                            for col in data.columns]
        
        current_time = datetime.now()
        data['last_updated'] = current_time
        
        data_dict = data.to_dict(orient='records')
        
        for record in data_dict:
            # Use the team name dynamically to access the correct keys
            date_key = f'For {team}_Date' 
            opponent_key = f'For {team}_Opponent'  
            
            date = record.get(date_key, record.get('Date', ''))
            opponent = record.get(opponent_key, record.get('Opponent', ''))
            
            if date and opponent:
                record['_id'] = f"{date}_{opponent}"
                print(f"Processing record: {record}") 
            
                # Check if the record already exists
                existing_record = collection.find_one({"_id": record['_id']})
                if existing_record:
                    print(f"Updating existing record: {record['_id']}")  
                else:
                    print(f"Inserting new record: {record['_id']}")  
                collection.update_one(
                    {"_id": record.get("_id", None)},
                    {"$set": record},
                    upsert=True
                )
        
        print(f"✅ Successfully updated {collection_name} collection with {len(data_dict)} records")
    else:
        print(f"⚠️ Skipping {collection_name} update - No valid data")
        pass
        
    print("✅ Database update complete")
