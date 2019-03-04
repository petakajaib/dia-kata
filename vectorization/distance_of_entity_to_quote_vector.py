from .utils import parse_text, get_text_position
import numpy as np

def get_entity_to_quote_distance(entity, quote_position, lowered_parsed_content):

    lowered_entity = entity.lower()
    parsed_lowered_entity = parse_text(lowered_entity)

    entity_position = get_text_position(lowered_parsed_content, parsed_lowered_entity)
    entity_to_quote_distance = abs(quote_position-entity_position)

    return entity_to_quote_distance


def get_quote_position(entry):
    content = entry["cleaned_content"]
    lowered_content = content.lower()
    quote = entry["quote"]

    parsed_content = parse_text(content)
    lowered_parsed_content = parse_text(lowered_content)
    parsed_quote = parse_text(quote.lower())

    quote_position = get_text_position(lowered_parsed_content, parsed_quote)

    return quote_position



def get_distance_of_entity_to_quote_vector(entry):

    quote_position = get_quote_position(entry)
    content = entry["cleaned_content"]
    lowered_content = content.lower()
    lowered_parsed_content = parse_text(lowered_content)

    vector = []

    for talker in entry["talker"]:
        distance_of_entity_to_quote = get_entity_to_quote_distance(talker["entity"], quote_position, lowered_parsed_content)
        vector.append(distance_of_entity_to_quote)

    return np.array(vector)
