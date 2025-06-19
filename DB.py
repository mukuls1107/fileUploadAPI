from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

def db_connection():
    try:
        print("Connecting the database...")
        db_url = os.getenv("DB_URL")
        
        if not db_url:
            print("ERROR: DB_URL not found in environment variables")
            return None
            
        client = MongoClient(db_url, server_api=ServerApi("1"))
        
        # Test connection
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        # Return the database object
        db = client.ez_database
        return db
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def get_collections():
    """Get list of all collections in the database"""
    try:
        db = db_connection()
        if db is not None:
            return db.list_collection_names()
        return []
    except Exception as e:
        print(f"Error getting collections: {e}")
        return []


db = db_connection()