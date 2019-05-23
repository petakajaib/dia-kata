import os
import pickle
from pymongo import MongoClient

MONGO_DB = "kronologi_malaysia"
ANNOY_INDEX_COLLECTION = "annoy_indexing"
QUOTE_COLLECTION = "quote"
ENTITY_KEYWORDS_COLLECTION = "entity_keywords"


client = MongoClient()

db = client[MONGO_DB]

target_path = os.environ.get("TARGET_DIRECTORY_PATH")

sample_entities = ["tun", "wan azizah", "anwar"]

annoy_index_collection = db[ANNOY_INDEX_COLLECTION]
annoy_entries = [entry for entry in annoy_index_collection.find()]

quote_collection = db[QUOTE_COLLECTION]
quote_query = {
    "talker": {"$in": sample_entities} 
}

quote_entries = [entry for entry in quote_collection.find(quote_query)]


entity_keywords_collection = db[ENTITY_KEYWORDS_COLLECTION]
entity_query = {
    "entity": {"$in": sample_entities}
}

keywords_entries = [entry for entry in 
                  entity_keywords_collection.find(entity_query)]

sample_data = {
    "annoy": annoy_entries,
    "quote": quote_entries,
    "keywords": keywords_entries
}

pickle.dump(sample_data, open(target_path, "wb"))