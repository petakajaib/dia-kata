from .utils import parse_text, get_text_position
import numpy as np

def get_entity_position_vector(entry):
    lowered_cleaned_content = entry["cleaned_content"].lower()

    parsed_content = parse_text(lowered_cleaned_content)
    vec = []

    for entity in entry["talker"]:

        parsed_entity = parse_text(entity["entity"].lower())
        position = get_text_position(parsed_content, parsed_entity)

        vec.append(position)

    return np.array(vec)
