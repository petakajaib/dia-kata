from polyglot.text import Text
import numpy as np

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

def vectorize_tokens(tokens, fasttext_model):

    shape = fasttext_model["a"].shape

    vec = np.zeros(shape)

    for t in tokens:
        try:
            vec = vec + fasttext_model[t]
        except KeyError as err:
            print(err)

    return vec/len(tokens)
