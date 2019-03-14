import json
from pprint import pprint
from itertools import combinations
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from nltk import ngrams
from scipy.spatial.distance import cosine
from sklearn.cluster import DBSCAN
import numpy as np
from settings import *

def preprocess_blob(blob):

    blob_ = blob.lower()
    blob_ = blob_.replace(" ", "")
    blob_ = blob_.replace(".", "")
    return blob_

def character_n_gram_tokenizer(blob, n_grams=(3,7)):

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

def create_tfidf_model(entities, n_grams_dictionary):

    dictionary_length = len(n_grams_dictionary)

    return TfidfModel(entity_bow_generator(entities, n_grams_dictionary))

def vectorize_entities(entities, tfidf_model, n_grams_dictionary):

    dictionary_length = len(n_grams_dictionary)
    vectors = []
    for idx, entity_ngrams_bow in enumerate(entity_bow_generator(entities, n_grams_dictionary)):

        vec = get_tfidf_vector(tfidf_model[entity_ngrams_bow], dictionary_length)

        vectors.append(vec)

    vectors = np.array(vectors)

    return vectors

def get_cluster_map(vectors, entities, eps, min_samples):

    cluster_map = {}
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    clustering.fit(vectors)

    for idx, label in enumerate(clustering.labels_):

        cluster_map[entities[idx]] = label

    return cluster_map

def clustering(entities, eps=0.9, min_samples=2, return_inverse=False):
    n_grams_dictionary = Dictionary(entity_ngrams_generator(entities))
    model = create_tfidf_model(entities, n_grams_dictionary)
    vectors = vectorize_entities(entities, model, n_grams_dictionary)
    cluster_map = {}

    if len(vectors):
        cluster_map = get_cluster_map(vectors, entities, eps, min_samples)

    if return_inverse:

        inverse_cluster_map = {}

        for key, value in cluster_map.items():
            if not inverse_cluster_map.get(value):
                inverse_cluster_map[value] = set()
            inverse_cluster_map[value].add(key)

        return cluster_map, inverse_cluster_map
    else:
        return cluster_map

if __name__ == '__main__':

    labelled_data = json.load(open(PREPROCESSED_PATH))

    for label in labelled_data:

        entities = [entity["entity"] for entity in label["talker"]]
        cluster_map = clustering(entities)

        pprint(cluster_map)
