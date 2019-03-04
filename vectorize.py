import json
import pickle
import numpy as np
from gensim.models.fasttext import FastText
from vectorization import (
    get_distance_of_entity_to_quote_vector,
    get_frequency_of_entity_vector,
    get_entity_position_vector,
    get_relative_frequency_ranking_vector,
    get_relative_entity_position_vector,
    get_quote_vector
)
from settings import *


def vectorize_feature(entry, fast_text_models):

    vecs = [
        get_distance_of_entity_to_quote_vector(entry),
        get_frequency_of_entity_vector(entry),
        get_entity_position_vector(entry),
        get_relative_frequency_ranking_vector(entry),
        get_relative_entity_position_vector(entry),
        get_quote_vector(entry, fast_text_models)
    ]

    # for vec in get_quote_vector(entry, fast_text_models):
    #     vecs.append(vec)

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

def vectorize_data(preprocessed_path, vectorized_path, fast_text_models):

    labelled_data = json.load(open(preprocessed_path))

    feature_vectors = []
    target_vectors = []

    total_entry = len(labelled_data)

    for idx, entry in enumerate(labelled_data):

        print("{} of {}        ".format(idx, total_entry))

        feature_vector = vectorize_feature(entry, fast_text_models)
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



if __name__ == '__main__':


    # print("loading fasttext models")
    # print("en")
    # en_fasttext = FastText.load(FASTTEXT_ENGLISH)
    #
    # print("ms")
    # ms_fasttext = FastText.load(FASTTEXT_MALAY)
    #
    # fast_text_models = {
    #     "en": en_fasttext,
    #     "ms": ms_fasttext
    # }

    fast_text_models = {}
    vectorize_data(PREPROCESSED_PATH, VECTORIZED_PATH, fast_text_models)


    # labelled_data = json.load(open(PREPROCESSED_PATH))
    #
    # feature_vectors = []
    # target_vectors = []
    #
    # total_entry = len(labelled_data)
    #
    # for idx, entry in enumerate(labelled_data):
    #
    #     print("{} of {}        ".format(idx, total_entry))
    #
    #     entity_position = get_entity_position_vector(entry)
    #     relative_entity_position = get_relative_entity_position_vector(entry)
    #
    #     raise ValueError("boom!")
