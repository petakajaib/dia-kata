import json
from itertools import combinations
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from nltk import ngrams
from scipy.spatial.distance import cosine
import numpy as np
from settings import *

def preprocess_blob(blob):

    blob_ = blob.lower()

    return blob_

def character_n_gram_tokenizer(blob, n_grams=(3,5)):

    blob = preprocess_blob(blob)

    list_of_ngrams = []

    for i in range(n_grams[0],n_grams[1]+1,1):
        l = [''.join(ngram) for ngram in ngrams(list(blob), i)]
        list_of_ngrams = l + list_of_ngrams

    return list_of_ngrams

def entity_ngrams_generator(entities):
    for entity in entities:
        yield character_n_gram_tokenizer(entity)

def entity_bow_generator(entities, dictionary):
    for n_grams in entity_ngrams_generator(entities):
        yield dictionary.doc2bow(n_grams)

def get_tfidf_vector(tfidf, dictionary_length):

    vec = np.zeros(dictionary_length)

    for idx, score in tfidf:
        vec[idx] = score

    return vec

labelled_data = json.load(open(PREPROCESSED_PATH))

for label in labelled_data:

    entities = [entity["entity"] for entity in label["talker"]]
    n_grams_dictionary = Dictionary(entity_ngrams_generator(entities))
    dictionary_length = len(n_grams_dictionary)
    # print("n_grams_dictionary length", dictionary_length)

    model = TfidfModel(entity_bow_generator(entities, n_grams_dictionary))

    vectors = []
    idx_map = {}
    for idx, entity_ngrams_bow in enumerate(entity_bow_generator(entities, n_grams_dictionary)):

        vec = get_tfidf_vector(model[entity_ngrams_bow], dictionary_length)

        idx_map[tuple(vec)] = idx

        vectors.append(vec)

    distances = []
    for vec_1, vec_2 in combinations(vectors, 2):

        distance = cosine(vec_1, vec_2)
        print(distance)

        print("entity_1", entities[idx_map[tuple(vec_1)]])
        print("entity_2", entities[idx_map[tuple(vec_2)]])
