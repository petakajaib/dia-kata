import numpy as np

def set_intersection(list_1, list_2):

    set_1 = set(list_1)
    set_2 = set(list_2)

    if set_1.intersection(set_2):
        return 1
    else:
        return 0

def get_title_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})
    title_tokens = article["lowered_title_tokens"]
    vec = []

    cleaned_content_entities_parsed = article["cleaned_content_entities_parsed"]

    for talker in entry["talker"]:
        entity_key = talker["entity"].lower().replace(".", "DOT")

        entity_tokens = [t.lower() for t in cleaned_content_entities_parsed[entity_key]]

        vec.append(set_intersection(title_tokens, entity_tokens))


    return np.array(vec)

def get_title_similarity_vector(entry, fast_text_models, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})
    title_tokens = article["lowered_title_tokens"]

    fast_text = fast_text_models[entry["language"]]

    title_vector = vectorize_tokens(title_tokens, fast_text)

    title_sim_vectors = []

    for talker in entry["talker"]:

        entity_key = talker["entity"].lower().replace(".", "DOT")
        entity_tokens = [token.lower() for token in article["cleaned_content_entities_parsed"][entity_key]]
        entity_vector = vectorize_tokens(entity_tokens, fast_text)
        semantic_distance = cosine(title_vector, entity_vector)

        title_sim_vectors.append(semantic_distance)

    return np.array(title_sim_vectors)
