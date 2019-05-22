import json
from flask import jsonify
from .queries import search_entities


def get_search_results(request, fasttext_entity,
                       annoy_index, annoy_index_collection):
    
    request_body = json.loads(request.body)
    query = request_body["query"]
    results = search_entities(
                query, fasttext_entity,
                annoy_index, annoy_index_collection)

    response = {"results": results}

    return jsonify(**response)
