from flask import Flask, jsonify, request
from pymongo import MongoClient
from gensim.models.fasttext import FastText
from annoy import AnnoyIndex
from first_time_jobs import search_entities
from settings import *

api = Flask(__name__)

dimension = 100

client = MongoClient()

db = client[MONGO_DB]
article_collection = db[MONGO_COLLECTION]
entity_collection = db[ENTITY_COLLECTION]
annoy_index_collection = db[ANNOY_INDEX_COLLECTION]
quote_collection = db[QUOTE_COLLECTION]
enriched_collection = db[MONGO_COLLECTION_ENRICHED]
similar_entities_collection = db[SIMILAR_ENTITIES_COLLECTION]
entity_keywords_collection = db[ENTITY_KEYWORDS_COLLECTION]

annoy_index = AnnoyIndex(dimension)
annoy_index.load(ANNOY_INDEX_PATH)
fasttext_entity = FastText.load(FASTTEXT_ENTITY)

@api.route("/search/", methods=['POST'])
def search():

    request_body = request.get_json()
    query = request_body["query"]
    results = search_entities(
                query, fasttext_entity,
                annoy_index, annoy_index_collection)

    d = {"results": results}
    return jsonify(**d)

@api.route("/detail/")
def detail():
    d[str(random())] = random()
    return jsonify(**d)

@api.route("/top_people/")
def top_people():
    return jsonify(top_people=["person1", "person2", "person3"])

@api.route("/fasttext/")
def reload_fasttext_models():
    return jsonify(ja=['pa'])

@api.route("/annoy/")
def reload_annoy_index():
    return jsonify(ja=['pa'])
