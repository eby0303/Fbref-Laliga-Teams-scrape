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
db = client['football']  # Database name

def check_if_scraping_needed(collection_name, hours_threshold=24):
    """
    Check if scraping is needed based on last update time
    Returns True if scraping is needed, False otherwise
    """
    try:
        collection = db[collection_name]
        
        # Check if collection exists and has documents
        if collection.count_documents({}) == 0:
            logger.info(f"Collection {collection_name} is empty. Scraping needed.")
            return True
            
        # Get the latest document
        latest_doc = collection.find_one(
            sort=[('last_updated', -1)]
        )
        
        # If no latest document found
        if not latest_doc:
            return True
            
        # Check if the data is older than threshold
        current_time = datetime.now()
        last_update = latest_doc.get('last_updated', datetime.min)
        
        if isinstance(last_update, str):
            last_update = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
            
        time_difference = current_time - last_update
        
        if time_difference > timedelta(hours=hours_threshold):
            logger.info(f"Data in {collection_name} is older than {hours_threshold} hours. Scraping needed.")
            return True
            
        logger.info(f"Recent data exists in {collection_name}. Skipping scrape.")
        return False
        
    except Exception as e:
        logger.error(f"Error checking collection {collection_name}: {e}")
        return True

def verify_database_connection():
    """Verify database connection and create indexes if needed"""
    try:
        # Test connection
        client.admin.command('ping')
        logger.info("✅ MongoDB connection successful")
        
        # Create indexes for each collection if they don't exist
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
        
        for collection_name in collections:
            collection = db[collection_name]
            # Create index on last_updated field
            collection.create_index('last_updated')
            logger.info(f"✅ Verified collection: {collection_name}")
            
        return True
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False

def update_data(scraped_data):
    """Update database with new scraped data"""
    try:
        for category, df in scraped_data.items():
            if df is not None and not df.empty:
                collection = db[category]
                
                # Flatten multi-level column names
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] 
                                for col in df.columns]
                
                # Add timestamp to each record
                current_time = datetime.now()
                df['last_updated'] = current_time
                
                # Convert DataFrame to records
                data_dict = df.to_dict(orient='records')
                
                # Create a unique identifier using Date and Opponent if available
                for record in data_dict:
                    try:
                        # Create a unique ID using Date and Opponent
                        date = record.get('For Barcelona_Date', record.get('Date', ''))
                        opponent = record.get('For Barcelona_Opponent', record.get('Opponent', ''))
                        if date and opponent:
                            record['_id'] = f"{date}_{opponent}"
                        
                        # Insert or update the record
                        result = collection.update_one(
                            {"_id": record.get("_id", None)},
                            {"$set": record},
                            upsert=True
                        )
                        
                    except Exception as e:
                        logger.error(f"❌ Error updating record in {category}: {e}")
                
                logger.info(f"✅ Successfully updated {category} collection with {len(data_dict)} records")
            else:
                logger.warning(f"⚠️ Skipping {category} update - No valid data")
                
        logger.info("✅ Database update complete")
        
    except Exception as e:
        logger.error(f"❌ Error updating database: {e}")
        raise

def get_collection_stats():
    """Get detailed statistics about all collections"""
    try:
        stats = {}
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            doc_count = collection.count_documents({})
            latest_doc = collection.find_one(sort=[('last_updated', -1)])
            
            stats[collection_name] = {
                'document_count': doc_count,
                'last_updated': latest_doc.get('last_updated', 'Never') if latest_doc else 'Never',
                'sample_fields': list(latest_doc.keys()) if latest_doc else [] if doc_count > 0 else None
            }
        return stats
    except Exception as e:
        logger.error(f"❌ Error getting collection stats: {e}")
        return {}

def view_collection_data(collection_name, limit=5):
    """View the most recent documents in a collection"""
    try:
        collection = db[collection_name]
        cursor = collection.find().sort('last_updated', -1).limit(limit)
        data = list(cursor)
        if data:
            df = pd.DataFrame(data)
            return df
        return None
    except Exception as e:
        logger.error(f"❌ Error viewing collection data: {e}")
        return None

if __name__ == "__main__":
    try:
        # Verify database connection and collections
        verify_database_connection()
        
        # Print collection statistics
        stats = get_collection_stats()
        logger.info("\n📊 Collection Statistics:")
        for collection, data in stats.items():
            logger.info(f"\n{collection}:")
            logger.info(f"  Documents: {data['document_count']}")
            logger.info(f"  Last Updated: {data['last_updated']}")
            if data['sample_fields']:
                logger.info(f"  Fields: {', '.join(data['sample_fields'])}")
                
            # Show sample data
            df = view_collection_data(collection)
            if df is not None and not df.empty:
                logger.info("\n  Sample Data (most recent):")
                logger.info(f"{df.head().to_string()}")
            
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")