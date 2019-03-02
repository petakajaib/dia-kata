from pymongo import MongoClient
from preprocessing import add_content_to_label
from settings import *

client = MongoClient()
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

print("preprocessing")

# add_content_to_label(LABELED_DATA_PATH, PREPROCESSED_PATH, collection)

print("vectorization")
