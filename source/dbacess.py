from pymongo import MongoClient

class BancoMongo:

    def __init__(self, URI):
        self.mongo_uri = URI
        self.client = MongoClient(self.mongo_uri)
        
    def setURI(self, URI):
        self.mongo_uri = URI
        self.client = MongoClient(self.mongo_uri)

    def setDb(self, db_name: str):
        #get a database
        self.db = self.client[db_name]

    def setCollection(self, collection_name: str):
        self.collection = self.db[collection_name]

    def saveQuestion(self, question: dict):
        self.collection.insert_one(question)