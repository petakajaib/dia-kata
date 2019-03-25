import numpy as np


def get_entity_is_in_quote(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})
    vec = []

    cleaned_content_entities = [ent.lower().replace(".", "DOT") for ent in article["cleaned_content_entities"]]

    for talker in entry["talker"]:
        entity = talker["entity"].lower().replace(".", "DOT")

        if entity in cleaned_content_entities:
            vec.append(1)
        else:
            vec.append(0)

    return np.array(vec)
