from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import flask


def db_connection():
    client = MongoClient(os.getenv("DB_URL"))
    db = client.ez_database
    dbNames = db.list_collection_names()
    return dbNames


