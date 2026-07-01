from pymongo import MongoClient
from config import Config

client=MongoClient(Config.MONGO_URI)

db=client[Config.DATABASE_NAME]

users_collection=db["users"]

tasks_collection=db["tasks"]