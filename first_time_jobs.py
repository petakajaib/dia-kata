from pymongo import MongoClient
from gensim.models.fasttext import FastText
from polyglot.text import Text
from settings import *
from datetime import datetime
import pycld2

def entity_generator(collection):
    for article in collection.find({"entities": {"$exists": True}}):
        yield article["entities"]

def populate_entity_collection(article_collection, entity_collection):
    query = {
        "publish_date": {"$gte": datetime(2019,4,5)},
        "content": {"$exists": True}
    }

    for article in article_collection.find(query):

        print(article["url"])

        if entity_collection.count({"url": article["url"]}) == 0:

            try:
                parsed = Text(article["content"])
                entities = [" ".join(entity) for entity in parsed.entities]

                entity = {
                    "entities": entities,
                    "url": article["url"],
                    "detected_language": parsed.detect_language(),
                    "publish_date": article["publish_date"]
                }

                entity_collection.insert_one(entity)

            except pycld2.error as err:
                print(err)
            except ValueError as err:
                print(err)
                continue

client = MongoClient()

db = client[MONGO_DB]
article_collection = db[MONGO_COLLECTION]
entity_collection = db[ENTITY_COLLECTION]

# populate_entity_collection(article_collection, entity_collection)

# For querying

# build fastText

fasttext_params = {
    "hs": 1,
    "window": 10,
    "min_count": 1,
    "workers": 7,
    "min_n": 1,
    "max_n": 10,
}

print("building corpus")

entity_corpus = [entity for entity in entity_generator(entity_collection)]
fasttext_entity = FastText(**fasttext_params)

print("count corpus")
fasttext_entity.build_vocab(sentences=entity_corpus)
total_examples = fasttext_entity.corpus_count

print("train fasttext")
fasttext_entity.train(sentences=entity_corpus, total_examples=total_examples, epochs=5)

print("saving fasttext")

fasttext_entity.save(FASTTEXT_ENTITY)

# build annoyIndex
#
