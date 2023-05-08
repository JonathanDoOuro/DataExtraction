from pymongo import MongoClient

# Create a MongoClient instance
mongo_uri = "mongodb://root:example@localhost:27017"
client = MongoClient(mongo_uri)

# Get a database
db = client.local

# Get a collection
collection = db.startup_log

# Query the collection
for document in collection.find():
    print(document)