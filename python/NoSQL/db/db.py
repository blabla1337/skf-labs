from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.comments_database

comments = db.comments_collection
users = db.users_collection
