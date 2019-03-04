import json
import re
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
                    print(entity_tokens)
                    print(token)
                    for entity_token in entity_tokens:
                        indices = [i for i, x in enumerate(tokens) if x == entity_token]
                        print("indices", indices)
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
