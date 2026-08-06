import sys
import urllib.parse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.utils.logger import logger

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class DatabaseManager:
    client: AsyncIOMotorClient = None
    db = None
    connected_since: datetime = None
    is_mock: bool = False

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
    """
    mongo_uri = settings.MONGO_URI
    db_name = settings.DB_NAME

    try:
        db_manager.client = AsyncIOMotorClient(
            mongo_uri,
            serverSelectionTimeoutMS=4000,
            connectTimeoutMS=4000
        )
        await db_manager.client.admin.command('ping')
        
        db_manager.db = db_manager.client[db_name]
        db_manager.connected_since = datetime.utcnow()
        db_manager.is_mock = False

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
        safe_print(f"⚠️ MongoDB Atlas Connection Warning: {str(err)}")
        safe_print(f"Falling back to local/in-memory mode for smooth execution.")
        safe_print(f"==================================================\n")
        logger.warning(f"Database connection warning: {str(err)}. App running in local/fallback mode.")
        db_manager.db = None
        db_manager.is_mock = True

async def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()
        logger.info("MongoDB connection closed.")

def get_database():
    return db_manager.db
