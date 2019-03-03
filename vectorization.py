import json
import pickle
from polyglot.text import Text
import numpy as np
from gensim.models.fasttext import FastText
from settings import *
from preprocessing import get_cleaned_content


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

def get_entity_position_vector(entry):
    lowered_cleaned_content = entry["cleaned_content"].lower()

    parsed_content = parse_text(lowered_cleaned_content)
    vec = []

    for entity in entry["talker"]:

        parsed_entity = parse_text(entity["entity"].lower())
        position = get_text_position(parsed_content, parsed_entity)

        vec.append(position)

    return np.array(vec)

def get_relative_frequency_ranking(entry):
    freq = get_frequency_of_entity_vector(entry)

    sorted_map = {}
    for idx, elem in enumerate(sorted(set(freq))):
        sorted_map[elem] = idx

    arr_relative = []
    for elem in freq:
        relative = sorted_map[elem]
        if relative == 0:
            arr_relative.append(1)
        else:
            arr_relative.append(1/relative)

    return np.array(arr_relative)

def vectorize_feature(entry):

    vecs = [
        get_distance_of_entity_to_quote_vector(entry),
        get_frequency_of_entity_vector(entry),
        get_entity_position_vector(entry),
        get_relative_frequency_ranking(entry)
    ]

    print(vecs)

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

def vectorize_data(preprocessed_path, vectorized_path):

    labelled_data = json.load(open(preprocessed_path))

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


    pickle.dump(vectorized, open(vectorized_path, "wb"))
    return vectorized

def vectorize_tokens(tokens, fasttext_model):

    shape = fasttext_model["a"].shape

    vec = np.zeros(shape)

    for t in tokens:
        try:
            vec = vec + fasttext_model[t]
        except KeyError as err:
            print(err)

    return vec/len(tokens)

def get_quote_vector(entry, fast_text_models):

    fast_text = fast_text_models[entry["language"]]

    cleaned_quote = get_cleaned_content(entry["quote"])
    parsed = Text(cleaned_quote)

    tokens = [str(token).lower() for token in parsed.tokens]

    quote_vectors = []

    for talker in entry["talker"]:
        quote_vector = vectorize_tokens(tokens, fast_text)

        quote_vectors.append(quote_vector)

    return np.array(quote_vectors)

if __name__ == '__main__':

    # vectorize_data(PREPROCESSED_PATH, VECTORIZED_PATH)

    print("loading fasttext models")
    print("en")
    en_fasttext = FastText.load(FASTTEXT_ENGLISH)

    print("ms")
    ms_fasttext = FastText.load(FASTTEXT_MALAY)

    fast_text_models = {
        "en": en_fasttext,
        "ms": ms_fasttext
    }

    labelled_data = json.load(open(PREPROCESSED_PATH))

    feature_vectors = []
    target_vectors = []

    total_entry = len(labelled_data)

    for idx, entry in enumerate(labelled_data):

        print("{} of {}        ".format(idx, total_entry))

        quote_vector = get_quote_vector(entry, fast_text_models)
        print("quote_vector", quote_vector.shape)
        frequency_of_entity_vector = get_frequency_of_entity_vector(entry)
        print("frequency_of_entity_vector", frequency_of_entity_vector)
        
        raise ValueError("boom!")
