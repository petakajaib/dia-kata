import json
import pickle
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

    return np.array(vector)

def get_token_count(cleaned_content, token):

    token = str(token).lower()

    parsed = Text(cleaned_content.lower())

    content_tokens = [str(t) for t in parsed.tokens]

    count = 0

    for content_token in content_tokens:

        if content_token == token:
            count  += 1

    return count


def get_frequency_of_entity_vector(entry):

    cleaned_content = entry["cleaned_content"]
    lowered_cleaned_content = cleaned_content.lower()

    vec = []

    for talker in entry["talker"]:
        parsed_entities = Text(talker["entity"].lower())

        counts = {}

        for token in parsed_entities.tokens:
            counts[token] = get_token_count(cleaned_content, token)

        avg = sum(counts.values())/len(counts.values())

        vec.append(avg)

    vec = np.array(vec)
    return vec

def vectorize_feature(entry):

    vecs = [
        get_distance_of_entity_to_quote_vector(entry),
        get_frequency_of_entity_vector(entry)
    ]

    vecs_reshaped = [v.reshape(v.shape[0], 1) for v in vecs]

    vec = np.hstack(vecs_reshaped)

    return vec

def vectorize_target(entry):

    target_vector = []

    for talker in entry["talker"]:

        if talker["correct"]:
            target_vector.append(1)
        else:
            target_vector.append(0)


    target_vector = np.array(target_vector)

    return target_vector.reshape(target_vector.shape[0], 1)


labelled_data = json.load(open(PREPROCESSED_PATH))

feature_vectors = []
target_vectors = []

total_entry = len(labelled_data)

for idx, entry in enumerate(labelled_data):

    print("{} of {}        ".format(idx, total_entry))

    feature_vector = vectorize_feature(entry)
    target_vector = vectorize_target(entry)

    if not len(target_vector):
        continue
    feature_vectors.append(feature_vector)
    target_vectors.append(target_vector)


vectorized = {
    "feature_vectors" : feature_vectors,
    "target_vectors": target_vectors
}


pickle.dump(vectorized, open(VECTORIZED_PATH, "wb"))
