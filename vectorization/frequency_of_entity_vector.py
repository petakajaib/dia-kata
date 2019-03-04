from polyglot.text import Text
import numpy as np
from .utils import parse_text

def get_token_count(cleaned_content_tokens, token):

    token = str(token).lower()

    count = 0

    for content_token in content_tokens:

        if content_token == token:
            count  += 1

    return count


def get_frequency_of_entity_vector(entry, enriched_collection):


    article = enriched_collection.find_one({"url":entry["source"]})

    cleaned_content = entry["cleaned_content"]

    cleaned_content_tokens = [t.lower() for t in parse_text(cleaned_content)]

    cleaned_content_tokens_db = [t.lower() for t in article["cleaned_content_tokens"]]

    cleaned_content_entities_parsed = article["cleaned_content_entities_parsed"]
    vec = []

    for talker in entry["talker"]:

        parsed_entities = Text(talker["entity"].lower())

        counts = {}

        for token in parsed_entities.tokens:
            counts[token] = get_token_count(cleaned_content_tokens, token)

        entity_key = talker["entity"].lower().replace(".", "DOT")
        counts_2 = {}
        for token in cleaned_content_entities_parsed[entity_key]:
            counts_2[token] = get_token_count(cleaned_content_tokens_db, token)

        assert counts == counts_2
        avg = sum(counts.values())/len(counts.values())

        vec.append(avg)

    vec = np.array(vec)
    return vec
