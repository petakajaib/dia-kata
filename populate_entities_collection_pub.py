from polyglot.text import Text
from pymongo import MongoClient
from redis import StrictRedis
import json
from settings import *

def populate_pub(article_collection, entity_collection, redis_client):
    query = {
        # "publish_date": {"$gte": datetime(2019,4,5)},
        "content": {"$exists": True}
    }

    for article in article_collection.find(query):

        print(article["url"])

        if entity_collection.count({"url": article["url"]}) == 0:
            del(article["_id"])
            redis_client.publish("populate_entities", json.dumps(article))


client = MongoClient()

db = client[MONGO_DB]
article_collection = db[MONGO_COLLECTION]
entity_collection = db[ENTITY_COLLECTION]
annoy_index_collection = db[ANNOY_INDEX_COLLECTION]

redis_client = StrictRedis()
# redis_pubsub = redis_client.pubsub()




populate_pub(article_collection, entity_collection, redis_client)
