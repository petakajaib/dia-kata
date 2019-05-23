import os
import pickle
from pymongo import MongoClient

MONGO_DB = "kronologi_malaysia"
ANNOY_INDEX_COLLECTION = "annoy_indexing"
QUOTE_COLLECTION = "quote"
ENTITY_KEYWORDS_COLLECTION = "entity_keywords"

client = MongoClient()

db = client[MONGO_DB]
annoy_index_collection = db[ANNOY_INDEX_COLLECTION]
quote_collection = db[QUOTE_COLLECTION]
entity_keywords_collection = db[ENTITY_KEYWORDS_COLLECTION]

target_path = os.environ.get("TARGET_DIRECTORY_PATH")
sample_data = pickle.load(open(target_path, "rb"))

annoy_index_collection.insert_many(sample_data["annoy"])
quote_collection.insert_many(sample_data["quote"])
entity_keywords_collection.insert_many(sample_data["keywords"])
