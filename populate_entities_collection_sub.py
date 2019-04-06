import json
from polyglot.text import Text
from pymongo import MongoClient
import pycld2
from redis import StrictRedis
from settings import *

def populate_sub(article, entity_collection):

    if entity_collection.count({"url": article["url"]}):
        return None

    try:
        parsed = Text(article["content"])
        entities = [" ".join(entity).lower() for entity in parsed.entities]

        entity = {
            "entities": entities,
            "url": article["url"],
            "detected_language": parsed.detect_language(),
            "publish_date": article["publish_date"]
        }

        entity_collection.insert_one(entity)
        return entity
    except pycld2.error as err:
        print(err)
    except ValueError as err:
        print(err)
        # continue

client = MongoClient()

db = client[MONGO_DB]

entity_collection = db[ENTITY_COLLECTION]
redis_client = StrictRedis()
redis_pubsub = redis_client.pubsub()

redis_pubsub.subscribe('populate_entities')

while True:

    message = redis_pubsub.get_message()                                               # Checks for message
    if message:
        data = message['data']
        # print(data)

        if data == 1:
            continue
        parsed = json.loads(data)
        entity = populate_sub(parsed, entity_collection)
        if entity:
            print(parsed["url"])
            print(entity["entities"])
