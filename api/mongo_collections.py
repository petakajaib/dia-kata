from pymongo import MongoClient
from settings import (
    MONGO_DB,
    MONGO_COLLECTION,
    ENTITY_COLLECTION,
    ANNOY_INDEX_COLLECTION,
    QUOTE_COLLECTION,
    MONGO_COLLECTION_ENRICHED,
    SIMILAR_ENTITIES_COLLECTION,
    ENTITY_KEYWORDS_COLLECTION
    )

client = MongoClient()

db = client[MONGO_DB]

article_collection = db[MONGO_COLLECTION]
entity_collection = db[ENTITY_COLLECTION]
annoy_index_collection = db[ANNOY_INDEX_COLLECTION]
quote_collection = db[QUOTE_COLLECTION]
enriched_collection = db[MONGO_COLLECTION_ENRICHED]
similar_entities_collection = db[SIMILAR_ENTITIES_COLLECTION]
entity_keywords_collection = db[ENTITY_KEYWORDS_COLLECTION]
