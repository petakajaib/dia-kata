from flask import jsonify
from quote_attribution_pipeline import get_similar_entities


def get_keywords_from_entity(entity, entity_keywords_collection):
    keyword_query = {
        "entity": entity
    }

    keywords_entry = entity_keywords_collection.find_one(
                        keyword_query,
                        sort=[("created_at", -1)])

    try:
        return keywords_entry["keywords"]
    except TypeError:
        return []


def get_quotes_from_entity(entity, quote_collection):

    quote_query = {
        "talker": entity,
    }

    quotes = [{"quote": q["quote"], "url": q["url"]} for q in
              quote_collection.find(
                    quote_query,
                    {
                        "quote": True,
                        "url": True,
                        "_id": False
                    }
                    ).sort("publish_time", -1)]

    return quotes


def get_detail(request_body, quote_collection, entity_keywords_collection,
               fasttext_entity, annoy_index, annoy_index_collection):

    entity = request_body["entity"]

    quotes = get_quotes_from_entity(entity, quote_collection)

    keywords = get_keywords_from_entity(
                    entity,
                    entity_keywords_collection)

    similar_entities = get_similar_entities(
        entity, fasttext_entity,
        annoy_index, annoy_index_collection)

    mentions = quote_collection.distinct("mentions", {"talker": entity})
    mentioned_by = quote_collection.distinct("talker", {"mentions": entity})

    response = {
        "entity": entity,
        "quotes": quotes,
        "keywords": keywords,
        "similar_entities": similar_entities,
        "mentions": mentions,
        "mentioned_by": mentioned_by
    }

    return jsonify(**response)
