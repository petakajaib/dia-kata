from itertools import chain
import numpy as np
from polyglot.text import Text
from settings import *

with open(SPEECH_VERB_PATH) as speech_verb_file:
    SPEECH_VERBS = speech_verb_file.read().split("\n")
    SPEECH_VERBS.remove("")

def get_speech_verb_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})

    cleaned_content_entities_parsed = article["cleaned_content_entities_parsed"]
    sentences_str = [[str(token).lower()for token in sent.tokens] for sent in Text(article["cleaned_content"]).sentences]

    grouped_sentences = []

    for i in range(len(sentences_str)):
        grouped_sentences.append(chain(*sentences_str[i:i+6]))

    vec = []

    for entity in entry["talker"]:
        entity_key = entity["entity"].lower().replace(".", "DOT")

        entity_tokens = cleaned_content_entities_parsed[entity_key]
        speech_verb = 0
        need_to_break = False
        for sentence in grouped_sentences:
            entity_is_in_sentence = all(elem in sentence for elem in entity_tokens)
            sentence_has_speech_verb = any(elem in SPEECH_VERBS for elem in sentence)
            if entity_is_in_sentence and sentence_has_speech_verb:
                speech_verb += 1
                break

        vec.append(speech_verb)

    return np.array(vec)

def get_speech_verb_relative_vector(entry, enriched_collection):
    freq = get_speech_verb_vector(entry, enriched_collection)

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
