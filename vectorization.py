import json
from polyglot.text import Text
import numpy as np
from settings import *

def parse_text(text):

    parsed = Text(text)

    return [str(token) for token in parsed.tokens]

def get_text_position(parsed_content, parsed_text):

    len_parsed_text = len(parsed_text)

    for idx, _ in enumerate(parsed_content):

        section = parsed_content[idx:idx+len_parsed_text]

        if section == parsed_text:
            return idx

        if len(section) != len_parsed_text:
            break


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

    return vector


def vectorize_feature(entry):

    vec_1 = get_distance_of_entity_to_quote_vector(entry)

    vec = np.array(vec_1)

    return vec

def vectorize_target(entry):

    target_vector = []

    for talker in entry["talker"]:

        if talker["correct"]:
            target_vector.append(1)
        else:
            target_vector.append(0)

    return np.array(target_vector)


labelled_data = json.load(open(PREPROCESSED_PATH))

for entry in labelled_data:
    feature_vector = vectorize_feature(entry)
    target_vector = vectorize_target(entry)

    print("feature_vector\n", feature_vector)
    print("target_vector\n", target_vector)
    print("===")
    break
