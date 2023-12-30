from pymongo import MongoClient
import os

def get_database():
    # MongoDB connection string from environment variable
    CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

    # Create a connection using MongoClient
    client = MongoClient("mongodb+srv://alcarrillop:XZIelxWz71C0JiSm@cluster0.ifc9oy8.mongodb.net/?retryWrites=true&w=majority")

    # Create the database if it doesn't exist
    return client['youtube_llm']

