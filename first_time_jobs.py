from pymongo import MongoClient
from polyglot.text import Text
from settings import *
from datetime import datetime

def article_generator(collection):

    for article in collection.find():

        yield article

client = MongoClient()

db = client[MONGO_DB]
article_collection = db[MONGO_COLLECTION]
entity_collection = db[ENTITY_COLLECTION]

query = {
    "publish_date": {"$gte": datetime(2019,4,5)},
    "language_detected": {"$in": ["ms", "en"]}
}

for article in collection.find(query):

    print(article["url"])

    if entity_collection.count({"url": article["url"]}) == 0:

        parsed = Text(article["content"])
        entities = [" ".join(entity) for entity in parsed.entities]

        entity = {
            "entities": entities,
            "url": article["url"]
        }

        entity_collection.insert_one(entity)



# For querying

# build fastText



# build annoyIndex

#
