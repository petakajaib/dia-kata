from .utils import parse_text, get_text_position
import numpy as np

def get_entity_position_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})

    lowered_cleaned_content = entry["cleaned_content"].lower()

    parsed_content = [t.lower() for t in article["cleaned_content_tokens"]]


    vec = []

    for entity in entry["talker"]:



        entity_key = entity["entity"].lower().replace(".", "DOT")

        parsed_entity = [t.lower()for t in article["cleaned_content_entities_parsed"][entity_key]]

        position = get_text_position(parsed_content, parsed_entity)

        vec.append(position)

    return np.array(vec)
