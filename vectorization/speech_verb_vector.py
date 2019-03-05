import numpy as np
from polyglot.text import Text
from settings import *

with open(SPEECH_VERB_PATH) as speech_verb_file:
    SPEECH_VERBS = speech_verb_file.read().split("\n")
    SPEECH_VERBS.remove("")

def get_speech_verb_vector(entry, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})

    cleaned_content_entities_parsed = article["cleaned_content_entities_parsed"]
    sentences = [Text(sent) for sent in article["cleaned_content_sentences"]]

    sentences_str = []

    for sentence in sentences:
        sentence_str = []

        for token in sentence.tokens:
            sentence_str.append(str(token).lower())

        sentences_str.append(sentence_str)

    vec = []

    for entity in entry["talker"]:
        entity_key = entity.lower().replace(".", "DOT")

        entity_tokens = cleaned_content_entities_parsed[entity_key]
        speech_verb = 0
        need_to_break = False
        for sentence in sentences_str:
            entity_is_in_sentence = all(elem in sentence for elem in entity_tokens)
            sentence_has_speech_verb = any(elem in SPEECH_VERBS for elem in sentence)
            if entity_is_in_sentence and sentence_has_speech_verb:
                speech_verb += 1
                break

        vec.append(speech_verb)

    return np.array(vec)
