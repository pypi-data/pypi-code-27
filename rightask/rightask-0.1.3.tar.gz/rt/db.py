import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.test_database
collection = db["dir_tree"]
