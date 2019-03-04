from .utils import parse_text, get_text_position
import numpy as np

def get_entity_position_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})

    lowered_cleaned_content = entry["cleaned_content"].lower()

    parsed_content = parse_text(lowered_cleaned_content)

    db_parsed_content = [t.lower() for t in article["cleaned_content_tokens"]]

    assert parsed_content == db_parsed_content

    vec = []

    for entity in entry["talker"]:

        parsed_entity = parse_text(entity["entity"].lower())


        entity_key = entity["entity"].lower().replace(".", "DOT")

        db_parsed_entity = [t.lower()for t in article["cleaned_content_entities_parsed"][entity_key]]

        assert parsed_entity == db_parsed_entity

        position = get_text_position(parsed_content, parsed_entity)

        vec.append(position)

    return np.array(vec)
