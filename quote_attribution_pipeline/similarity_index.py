from datetime import timedelta
from annoy import AnnoyIndex


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


def build_annoy_index(collection, annoy_index_collection,
                      fasttext_entity, dimension, annoy_index_path):

    annoy_index = AnnoyIndex(dimension)

    annoy_index_collection.delete_many({})

    for idx, entity in enumerate(collection.distinct("talker", {})):

        if annoy_index_collection.count({"entity": entity}) == 0:
            annoy_index_collection.insert_one({
                "idx": idx,
                "entity": entity
                })

            vector = fasttext_entity[entity]

            annoy_index.add_item(idx, vector)

    annoy_index.build(10)
    annoy_index.save(annoy_index_path)

    return annoy_index


def populate_similar_entities(
        talkers,
        query_date,
        fasttext_entity,
        annoy_index,
        quote_collection,
        similar_entities_collection,
        annoy_index_collection
        ):

    count_talkers = len(talkers)

    for idx, talker in enumerate(talkers):

        if similar_entities_collection.count({
                "entity": talker,
                "created_at": {
                    "$gte": query_date,
                    "$lt": query_date + timedelta(days=1)
                    }
                }) > 0:

            continue

        print("populate similar entities {} of {}. entity: {}".format(
            idx,
            count_talkers,
            talker
        ))
        similar_entities = get_similar_entities(
            talker, fasttext_entity,
            annoy_index, annoy_index_collection,
            )

        similar_entry = {
            "entity": talker,
            "similar": similar_entities,
            "created_at": query_date
        }
        similar_entities_collection.insert_one(similar_entry)
