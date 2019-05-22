import json
from flask import jsonify
from .queries import get_similar_entities


def get_detail(request, quote_collection, entity_keywords_collection,
               fasttext_entity, annoy_index, annoy_index_collection):

    request_body = json.loads(request.content)
    entity = request_body["entity"]

    quote_query = {
        "talker": entity,
    }

    quotes = [q["quote"] for q in quote_collection.find(quote_query).sort("publish_time", -1)]

    keyword_query = {
        "entity": entity
    }

    keywords_entry = entity_keywords_collection.find_one(keyword_query, sort=[("created_at", -1)])

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
