from pymongo.mongo_client import MongoClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URL)
db = client.todo_db
collection_name = db["todo_collection"]
