import json
from polyglot.text import Text
import numpy as np
from settings import *

def parse_text(text):

    parsed = Text(text)

    return [str(token) for token in parsed.tokens]

def get_text_position(parsed_content, parsed_text):

    print("get_text_position")

    print("parsed_content", parsed_content)
    print("parsed_text", parsed_text)


    len_parsed_text = len(parsed_text)

    for idx, _ in enumerate(parsed_content):

        section = parsed_content[idx:idx+len_parsed_text]

        if section == len_parsed_text:
            return idx

        if len(section) != len_parsed_text:
            break


def distance_of_entity_to_quote(entry):

    content = entry["cleaned_content"]
    lowered_content = content.lower()
    quote = entry["quote"]

    parsed_content = parse_text(content)
    lowered_parsed_content = parse_text(lowered_content)
    parsed_quote = parse_text(quote.lower())

    quote_position = get_text_position(lowered_content, parsed_quote)
    print("quote_position", quote_position)
    vector = []

    for talker in entry["talker"]:
        entity = talker["entity"]
        lowered_entity = entity.lower()
        parsed_lowered_entity = parse_text(lowered_entity)

        position = get_text_position(lowered_parsed_content, parsed_lowered_entity)
        print("entity position", position)
        entity_position = abs(quote_position-position)
        vector.append(entity_position)

    return vector

def vectorize_feature(entry):

    vec_1 = distance_of_entity_to_quote(entry)

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


    break
