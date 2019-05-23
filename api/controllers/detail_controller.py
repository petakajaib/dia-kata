from flask import jsonify
from .queries import (
    get_similar_entities,
    get_quotes_from_entity,
    get_keywords_from_entity
)


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
