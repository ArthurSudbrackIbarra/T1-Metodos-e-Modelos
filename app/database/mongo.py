from pymongo import MongoClient
from pymongo.database import Database
from mongomock import MongoClient as MockMongoClient
from app.config import settings


# This function returns the database.
# With the database object we can access collections.
# We can also create/delete new collections.
#
# Depending on the value of settings.DB_ENVIRONMENT variable,
# a mocked database will be returned instead of the real database.
def get_database() -> Database:
    if str.lower(settings.DB_ENVIRONMENT) == "test":
        return get_mock_database()
    return get_real_database()


# This function returns the real database.
def get_real_database() -> Database:
    # Connect to MongoDB.
    _client = MongoClient(settings.DB_HOST)
    # Access database.
    _database = _client[settings.DB_NAME]
    return _database


# This function returns a mock database.
# It is used for testing.
def get_mock_database() -> Database:
    _client = MockMongoClient()
    _database = _client[settings.DB_NAME]
    return _database
