from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
#client = MongoClient("mongodb://mongo:27017/")
db = client["biblioteca"]