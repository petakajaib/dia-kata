import numpy as np


def get_is_person_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})
    vec = []

    cleaned_content_entities_tag = article["cleaned_content_entities_tag"]

    for talker in entry["talker"]:
        entity_key = talker["entity"].lower().replace(".", "DOT")

        entity_tag = cleaned_content_entities_tag[entity_key]

        if entity_tag == "I-PER":
            vec.append(1)
        else:
            vec.append(0)

    return np.array(vec)

def get_is_organization_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})
    vec = []

    cleaned_content_entities_tag = article["cleaned_content_entities_tag"]

    for talker in entry["talker"]:
        entity_key = talker["entity"].lower().replace(".", "DOT")

        entity_tag = cleaned_content_entities_tag[entity_key]

        if entity_tag == "I-ORG":
            vec.append(1)
        else:
            vec.append(0)

    return np.array(vec)

def get_is_location_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})
    vec = []

    cleaned_content_entities_tag = article["cleaned_content_entities_tag"]

    for talker in entry["talker"]:
        entity_key = talker["entity"].lower().replace(".", "DOT")

        entity_tag = cleaned_content_entities_tag[entity_key]

        if entity_tag == "I-LOC":
            vec.append(1)
        else:
            vec.append(0)

    return np.array(vec)
