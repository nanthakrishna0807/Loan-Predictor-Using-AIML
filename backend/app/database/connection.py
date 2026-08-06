import sys
import os
import urllib.parse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

# Ensure backend directory is in sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
root_dir = os.path.dirname(backend_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from app.config.settings import settings
    from app.utils.logger import logger
except ModuleNotFoundError:
    from backend.app.config.settings import settings
    from backend.app.utils.logger import logger

# Ensure Windows terminal handles UTF-8 emojis cleanly
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class DatabaseManager:
    client: AsyncIOMotorClient = None
    db = None
    connected_since: datetime = None

db_manager = DatabaseManager()

def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        clean_text = text.encode('ascii', 'ignore').decode('ascii')
        print(clean_text)

async def connect_to_mongo():
    """
    Establishes connection to MongoDB Atlas using Motor async driver.
    Displays formatted console outputs on success or failure.
    """
    mongo_uri = settings.MONGO_URI
    db_name = settings.DB_NAME

    try:
        db_manager.client = AsyncIOMotorClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )
        await db_manager.client.admin.command('ping')
        
        db_manager.db = db_manager.client[db_name]
        db_manager.connected_since = datetime.utcnow()

        collections = await db_manager.db.list_collection_names()
        collection_count = len(collections)

        host = "Atlas Cluster"
        try:
            parsed = urllib.parse.urlparse(mongo_uri)
            if parsed.hostname:
                host = parsed.hostname
        except Exception:
            pass

        safe_print(f"\n==================================================")
        safe_print(f"✅ MongoDB Atlas Connected Successfully")
        safe_print(f"Database: {db_name}")
        safe_print(f"Host: {host}")
        safe_print(f"Collections: {collection_count}")
        safe_print(f"==================================================\n")

        logger.info(f"Database connected successfully to {db_name} at {host}")

    except Exception as err:
        safe_print(f"\n==================================================")
        safe_print(f"❌ MongoDB Connection Failed")
        safe_print(f"Reason: {str(err)}")
        safe_print(f"Possible Causes:")
        safe_print(f"- Invalid URI")
        safe_print(f"- Authentication Failed")
        safe_print(f"- Atlas Cluster Paused")
        safe_print(f"- IP Not Whitelisted")
        safe_print(f"==================================================\n")

        logger.error(f"Database connection failed: {str(err)}")
        sys.exit(1)

async def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()
        logger.info("MongoDB Atlas connection closed.")

def get_database():
    return db_manager.db
