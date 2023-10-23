import os

from pymongo import MongoClient

mongo_user = os.getenv("MONGODB_USER")
mongo_pass = os.getenv("MONGODB_PASSWORD")
mongo_host = os.getenv("MONGODB_HOST")
mongo_port = os.getenv("MONGODB_PORT")
mongo_db = os.getenv("MONGODB_DATABASE")

uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client[mongo_db]


def get_mongo_collection():
    return db.get_collection("todo_collection")
