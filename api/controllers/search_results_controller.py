from .queries import search_entities


def get_search_results(request, fasttext_entity,
                       annoy_index, annoy_index_collection):
    request_body = request.get_json()
    query = request_body["query"]
    results = search_entities(
                query, fasttext_entity,
                annoy_index, annoy_index_collection)

    response = {"results": results}

    return response
