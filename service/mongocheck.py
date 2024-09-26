from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')  # Or your MongoDB Atlas URI
db = client.contacts_db
print("Connection successful!")
