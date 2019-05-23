from flask import jsonify
from .queries import search_entities


def get_search_results(request_body, fasttext_entity,
                       annoy_index, annoy_index_collection):

    query = request_body["query"]
    results = search_entities(
                query, fasttext_entity,
                annoy_index, annoy_index_collection)

    response = {"results": results, "query": query}

    return jsonify(**response)
