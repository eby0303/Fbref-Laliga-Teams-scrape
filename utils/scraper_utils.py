import logging
import pandas as pd
from functools import wraps
import time
import importlib

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = ['pandas', 'lxml', 'requests', 'bs4']
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        raise ImportError(
            f"Missing required dependencies: {', '.join(missing_packages)}. "
            f"Please install using: pip install {' '.join(missing_packages)}"
        )

def safe_read_html(url, table_id):
    """Safely read HTML table with proper error handling"""
    try:
        check_dependencies()
        return pd.read_html(url, attrs={'id': table_id})
    except ImportError as e:
        logger.error(f"Dependency Error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error reading HTML table: {e}")
        raise

def validate_scrape(df, module_name):
    """Basic validation to check if scraping worked"""
    logger = logging.getLogger(module_name)
    
    if df is None or df.empty:
        logger.error(" Scraping failed: DataFrame is empty or None")
        return False
    
    logger.info(f" Scraping successful! Retrieved {len(df)} rows of data")
    return True

def retry_on_failure(max_retries=3, delay=5):
    """Decorator to retry failed scraping attempts"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            
            for attempt in range(max_retries):
                try:
                    logger.info(f" Attempt {attempt + 1} of {max_retries}")
                    result = func(*args, **kwargs)
                    return result
                except ImportError as e:
                    logger.error(f" Dependency Error: {e}")
                    raise  # Don't retry if it's a dependency issue
                except Exception as e:
                    logger.error(f" Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        logger.info(f" Waiting {delay} seconds before retrying...")
                        time.sleep(delay)
                    else:
                        logger.error(" All retry attempts failed")
                        raise
            
        return wrapper
    return decorator 