from flask import Flask, jsonify, request
from pymongo import MongoClient
from gensim.models.fasttext import FastText
from annoy import AnnoyIndex
from first_time_jobs import search_entities, get_similar_entities
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

    response = {"results": results}

    return jsonify(**response)

@api.route("/detail/", methods=['POST'])
def detail():
    request_body = request.get_json()
    entity = request_body["entity"]

    quote_query = {
        "talker": entity,
    }

    quotes = [q["quotes"] for q in quote_collection.find(quote_query).sort("publish_time", -1).limit(10)]

    keyword_query = {
        "entity": entity
    }

    keywords_entry = entity_keywords_collection.find_one(keyword_query).sort("created_at", -1)

    mentions = quote_collection.distinct("mentions", {"talker": entity})
    mentioned_by = quote_collection.distinct("talker", {"mentions": entity})
    similar_entities = get_similar_entities(
        entity, fasttext_entity,
        annoy_index, annoy_index_collection)

    response = {
        "entity": entity,
        "quotes": quotes,
        "keywords": keywords_entry["keywords"],
        "similar_entities": similar_entities,
        "mentions": mentions,
        "mentioned_by": mentioned_by
    }

    return jsonify(**response)

@api.route("/top_people/")
def top_people():
    return jsonify(top_people=["person1", "person2", "person3"])

# @api.route("/fasttext/")
# def reload_fasttext_models():
#     return jsonify(ja=['pa'])
#
# @api.route("/annoy/")
# def reload_annoy_index():
#     return jsonify(ja=['pa'])
