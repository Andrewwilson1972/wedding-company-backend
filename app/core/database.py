from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Global variables to hold DB client and database reference
client: AsyncIOMotorClient | None = None
db = None


def connect_to_mongo():
    """
    Initialize MongoDB connection using Motor (async).
    Called when the app starts.
    """
    global client, db
    print(f"Connecting to MongoDB at: {settings.mongo_uri}")
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client.get_default_database()
    return db


def get_db():
    """
    Returns the database instance.
    If it's not initialized yet, initializes it.
    """
    global db
    if db is None:
        return connect_to_mongo()
    return db
