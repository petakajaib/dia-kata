from flask import jsonify


def search_entities(
        query, fasttext_entity,
        annoy_index, annoy_index_collection,
        n_results=20):

    vector = fasttext_entity[query]

    aggregated = []
    for result in annoy_index.get_nns_by_vector(vector, n_results):

        res = annoy_index_collection.find_one({"idx": result})
        aggregated.append(res["entity"])

    return aggregated[:n_results]


def get_search_results(request_body, fasttext_entity,
                       annoy_index, annoy_index_collection):

    query = request_body["query"]
    results = search_entities(
                query, fasttext_entity,
                annoy_index, annoy_index_collection)

    response = {"results": results, "query": query}

    return jsonify(**response)
