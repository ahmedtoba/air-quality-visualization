from datetime import time
from pymongo import MongoClient
from dotenv import load_dotenv
from app.config import Config
from pymongo.errors import AutoReconnect

# Load environment variables
load_dotenv()

def get_mongo_client():
    """Create and return a MongoDB client using environment variables."""
    host = Config.MONGO_HOST
    port = Config.MONGO_PORT
    username = Config.MONGO_USERNAME
    password = Config.MONGO_PASSWORD
    auth_source = Config.MONGO_AUTH_SOURCE

    # Initialize the MongoClient with the credentials
    retries = 3
    while retries > 0:
        try:
            client = MongoClient(
                host = host,
                port = port,
                username = username,
                password = password,
                authSource = auth_source,
            )
            return client
        except AutoReconnect:
            retries -= 1
            time.sleep(1)

    return client

def get_database():
    client = get_mongo_client()
    return client[Config.MONGO_DB_NAME]
