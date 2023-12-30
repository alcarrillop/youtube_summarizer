from pymongo import MongoClient
import os

def get_database():
    # MongoDB connection string from environment variable
    CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database if it doesn't exist
    return client['youtube_llm']

