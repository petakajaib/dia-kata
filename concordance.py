import json
import re
from itertools import combinations
from pymongo import MongoClient
from nltk import word_tokenize, sent_tokenize
from settings import *


client = MongoClient()
db = client[MONGO_DB]
enriched_collection = db[MONGO_COLLECTION_ENRICHED]

label = json.load(open(LABELED_DATA_PATH))

concordance = {}

for entry in label:

    url = entry["source"]
    article = enriched_collection.find_one({"url": url})

    content = article["cleaned_content"]
    cleaned_content_entities_parsed = article["cleaned_content_entities_parsed"]
    sentences = sent_tokenize(content)

    for entity in entry["talker"]:

        entity_key = entity["entity"].lower().replace(".", "DOT")

        entity_tokens = cleaned_content_entities_parsed[entity_key]

        if entity["correct"]:

            for sentence in sentences:

                tokens = word_tokenize(sentence.lower())


                all_in = True

                for entity_token in entity_tokens:
                    if entity_token not in tokens:
                        all_in = False

                if all_in:


                    flattened_indices = []
                    for entity_token in entity_tokens:
                        indices = [i for i, x in enumerate(tokens) if x == entity_token]

                        for idx in indices:
                            flattened_indices.append(idx)

                    matched_indices = None

                    if len(entity_tokens) == 1:
                        # print("indices:", flattened_indices)
                        matched_indices = flattened_indices
                    elif len(entity_tokens) > 1:
                        list_indices = []
                        for indices in combinations(flattened_indices, len(entity_tokens)):
                            sorted_indices = sorted(indices)
                            diffs = []

                            for idx in range(0, len(entity_tokens)-1):
                                diffs.append(abs(sorted_indices[idx]-sorted_indices[idx+1]))

                            all_is_one = True

                            for diff in diffs:
                                if diff != 1:
                                    all_is_one = False

                            if all_is_one:
                                list_indices.append(sorted_indices)

                        # print("list_indices", list(set([tuple(l)for l in list_indices])))
                        matched_indices = list_indices

                    if matched_indices:

                        for idx in matched_indices:

                            if type(idx) == int:
                                begin_idx = idx - 5
                                if begin_idx < 0:
                                    begin_idx = 0

                                end_idx = idx + 5
                                if end_idx > len(tokens):
                                    end_idx = len(tokens)

                                concordance = tokens[begin_idx:end_idx]

                            elif type(idx) == tuple:

                                print("tuple indices", idx)
                                begin_idx = idx[0] - 5
                                if begin_idx < 0:
                                    begin_idx = 0

                                end_idx = idx[-1] + 5
                                if end_idx > len(tokens):
                                    end_idx = len(tokens)

                                concordance = tokens[begin_idx:end_idx]
                            print("entity_tokens:", entity_tokens)
                            # print("tokens", tokens)
                            print("concordance:", concordance)

                # for match in re.finditer(entity_key, sentence):
                #     span = match.span()
                #     begin_match, end_match = span
                #
                #     len_sentence = len(sentence)

                    # begin = abs(begin_match - 20)
                    # end = end_match + 20
                    #
                    # if end > len_sentence:
                    #     end = len_sentence

                    # print(entity_key)
                    # print(sentence[begin:end])
