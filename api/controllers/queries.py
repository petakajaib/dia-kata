
def get_keywords_from_entity(entity, entity_keywords_collection):
    keyword_query = {
        "entity": entity
    }

    keywords_entry = entity_keywords_collection.find_one(
                        keyword_query,
                        sort=[("created_at", -1)])

    return keywords_entry["keywords"]


def get_quotes_from_entity(entity, quote_collection):

    quote_query = {
        "talker": entity,
    }

    quotes = [{"quote": q["quote"], q["url"]} for q in
              quote_collection.find(
                    quote_query,
                    {
                        "quote": True,
                        "url": True,
                        "_id": False
                    }
                    ).sort("publish_time", -1)]

    return quotes


def get_similar_entities(
        query, fasttext_entity,
        annoy_index, annoy_index_collection,
        n_results=10):

    vector = fasttext_entity[query]

    aggregated = []
    for result in annoy_index.get_nns_by_vector(vector, 500):

        res = annoy_index_collection.find_one({"idx": result})

        query_set = set(query.lower().split())
        entity_set = set(res["entity"].split())

        if query in res["entity"]:
            continue
        if len(query_set.intersection(entity_set)):
            continue
        else:
            aggregated.append(res["entity"])

    return aggregated[:n_results]


def search_entities(
        query, fasttext_entity,
        annoy_index, annoy_index_collection,
        n_results=20):

    vector = fasttext_entity[query]

    aggregated = []
    for result in annoy_index.get_nns_by_vector(vector, n_results):

        res = annoy_index_collection.find_one({"idx": result})

        query_set = set(query.lower().split())
        entity_set = set(res["entity"].split())

        aggregated.append(res["entity"])

    return aggregated[:n_results]
