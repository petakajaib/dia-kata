import numpy as np

def jaccard_divergence(list_1, list_2):

    set_1 = set(list_1)
    set_2 = set(list_2)

    return len(set_1.intersection(set_2))/len(set_1.union(set_2))

def get_title_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})
    title_tokens = article["lowered_title_tokens"]
    vec = []

    cleaned_content_entities_parsed = article["cleaned_content_entities_parsed"]

    for talker in entry["talker"]:
        entity_key = talker["entity"].lower().replace(".", "DOT")

        entity_tokens = [t.lower() for t in cleaned_content_entities_parsed[entity_key]]

        vec.append(jaccard_divergence(title_tokens, entity_tokens))


    return np.array(vec)
