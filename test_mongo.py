import sys
import os
from pymongo import MongoClient
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

try:
    client.admin.command("ping")
    print("✅ MongoDB Atlas Connected Successfully")
    print("Available Databases:", client.list_database_names())
except Exception as e:
    print("❌ Connection Failed")
    print(e)
