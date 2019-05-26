from polyglot.text import Text
import numpy as np
from scipy.spatial.distance import cosine
from ml_pipeline.preprocessing import get_cleaned_content
from .utils import vectorize_tokens


def get_quote_vector(entry, fast_text_models, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})

    fast_text = fast_text_models[entry["language"]]

    cleaned_quote = get_cleaned_content(entry["quote"])
    parsed = Text(cleaned_quote)

    tokens = [str(token).lower() for token in parsed.tokens]
    quote_vector = vectorize_tokens(tokens, fast_text)

    quote_vectors = []

    for talker in entry["talker"]:

        entity_key = talker["entity"].lower().replace(".", "DOT")
        entity_tokens = [token.lower() for token in article["cleaned_content_entities_parsed"][entity_key]]

        entity_vector = vectorize_tokens(entity_tokens, fast_text)
        semantic_distance = cosine(quote_vector, entity_vector)

        quote_vectors.append(semantic_distance)

    return np.array(quote_vectors)

def get_quote_relative_vector(entry, fast_text_models, enriched_collection):
    quote_sim = get_quote_vector(entry, fast_text_models, enriched_collection)

    sorted_map = {}
    for idx, elem in enumerate(sorted(set(quote_sim), reverse=True)):
        sorted_map[elem] = idx

    arr_relative = []
    for elem in quote_sim:
        relative = sorted_map[elem]
        if relative == 0:
            arr_relative.append(1)
        else:
            arr_relative.append(1/relative)

    return np.array(arr_relative)
