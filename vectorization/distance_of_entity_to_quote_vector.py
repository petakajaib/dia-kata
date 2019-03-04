from .utils import parse_text, get_text_position
import numpy as np

def get_entity_to_quote_distance(entity, quote_position, lowered_parsed_content, enriched_collection):

    article = enriched_collection.find_one({"url": entity["source"]})

    lowered_entity = entity.lower()

    entity_key = lowered_entity.replace(".", "DOT")

    parsed_lowered_entity = parse_text(lowered_entity)
    print("parsed_lowered_entity", parsed_lowered_entity)

    print("db backed parsed_lowered_entity", article["cleaned_content_entities_parsed"][entity_key])

    entity_position = get_text_position(lowered_parsed_content, parsed_lowered_entity)
    entity_to_quote_distance = abs(quote_position-entity_position)

    return entity_to_quote_distance


def get_quote_position(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})

    content = entry["cleaned_content"]
    lowered_content = content.lower()
    quote = entry["quote"]

    parsed_content = parse_text(content)
    lowered_parsed_content = parse_text(lowered_content)
    print("lowered_parsed_content get_quote_position", lowered_parsed_content)
    print("db lowered_parsed_content get_quote_position", [t.lower() for t in article["cleaned_content_tokens"]])
    parsed_quote = parse_text(quote.lower())

    quote_position = get_text_position(lowered_parsed_content, parsed_quote)

    return quote_position



def get_distance_of_entity_to_quote_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})

    quote_position = get_quote_position(entry, enriched_collection)
    content = entry["cleaned_content"]
    lowered_content = content.lower()
    lowered_parsed_content = parse_text(lowered_content)

    print("lowered_parsed_content get_distance_of_entity_to_quote_vector", lowered_parsed_content)

    print("db lowered_parsed_content", [t.lower() for t in article["cleaned_content_tokens"]])

    vector = []

    for talker in entry["talker"]:
        distance_of_entity_to_quote = get_entity_to_quote_distance(talker["entity"], quote_position, lowered_parsed_content, enriched_collection)
        vector.append(distance_of_entity_to_quote)

    return np.array(vector)
