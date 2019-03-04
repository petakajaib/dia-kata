from polyglot.text import Text
import numpy as np
from scipy.spatial.distance import cosine
from preprocessing import get_cleaned_content
from .utils import vectorize_tokens

def get_quote_vector(entry, fast_text_models, enriched_collection):

    article = enriched_collection.find_one({"url": entry["source"]})

    fast_text = fast_text_models[entry["language"]]

    cleaned_quote = get_cleaned_content(entry["quote"])
    parsed = Text(cleaned_quote)

    tokens = [str(token).lower() for token in parsed.tokens]

    db_tokens = [t.lower() for t in article["cleaned_content_tokens"]]

    try:
        assert db_tokens == tokens
    except AssertionError as err:
        print(tokens)
        print(db_tokens)
        raise err
    quote_vectors = []

    for talker in entry["talker"]:
        quote_vector = vectorize_tokens(tokens, fast_text)
        entity_tokens = [str(token).lower() for token in Text(talker["entity"]).tokens]

        entity_key = talker["entity"].lower().replace(".", "DOT")
        db_entity_tokens = [token.lower() for token in article["cleaned_content_entities_parsed"]]

        try:
            assert entity_tokens == db_entity_tokens
        except AssertionError as err:
            print(entity_tokens)
            print(db_entity_tokens)
            raise err
        entity_vector = vectorize_tokens(entity_tokens, fast_text)
        semantic_distance = cosine(quote_vector, entity_vector)

        quote_vectors.append(semantic_distance)

    return np.array(quote_vectors)
