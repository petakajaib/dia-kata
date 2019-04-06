from datetime import datetime
from annoy import AnnoyIndex
from gensim.models.fasttext import FastText
from polyglot.text import Text
import numpy as np
import pycld2
from pymongo import MongoClient
from redis import StrictRedis
from settings import *

def entity_generator(collection):
    for article in collection.find({"entities": {"$exists": True}}):
        yield article["entities"]

def populate_entity_collection(article_collection, entity_collection):
    query = {
        # "publish_date": {"$gte": datetime(2019,4,5)},
        "content": {"$exists": True}
    }

    for article in article_collection.find(query, no_cursor_timeout=True):

        print(article["url"])

        if entity_collection.count({"url": article["url"]}) == 0:

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

            except pycld2.error as err:
                print(err)
            except ValueError as err:
                print(err)
                continue

def build_fast_text_model():
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

    return fasttext_entity

def build_annoy_index():
    dimension = 100
    annoy_index = AnnoyIndex(dimension)

    idx = 1
    annoy_index_collection.delete_many({})

    for entities in entity_generator(entity_collection):

        for entity in entities:

            if annoy_index_collection.count({"entity": entity}) == 0:

                print("{}\t{}          ".format(idx, entity), end="\r")

                annoy_index_collection.insert_one({
                    "idx": idx,
                    "entity": entity
                    })

                vector = fasttext_entity[entity]

                annoy_index.add_item(idx, vector)

                idx += 1

    print("{}\t{}          ".format(idx, entity))

    annoy_index.build(10)
    annoy_index.save(ANNOY_INDEX_PATH)

client = MongoClient()

db = client[MONGO_DB]
article_collection = db[MONGO_COLLECTION]
entity_collection = db[ENTITY_COLLECTION]
annoy_index_collection = db[ANNOY_INDEX_COLLECTION]

populate_entity_collection(article_collection, entity_collection)

build_fast_text_model()
fasttext_entity = FastText.load(FASTTEXT_ENTITY)

# build annoyIndex
#
build_annoy_index()
dimension = 100
annoy_index = AnnoyIndex(dimension)

annoy_index.load(ANNOY_INDEX_PATH)

sample_query = "wan azizah"

tokens = sample_query.split()
vector = np.zeros(dimension)

for tok in tokens:
    tok_vector = fasttext_entity[sample_query]
    vector = vector + tok_vector

vector = vector/len(tokens)

n = 100

aggregated = []
print("query:", sample_query)
for result in annoy_index.get_nns_by_vector(vector, n):

    res = annoy_index_collection.find_one({"idx": result})

    if sample_query in res["entity"]:
        continue
    else:
        aggregated.append(res["entity"])

print(aggregated[:10])
