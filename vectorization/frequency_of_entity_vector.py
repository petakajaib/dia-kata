from polyglot.text import Text
import numpy as np

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
