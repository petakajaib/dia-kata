import json
import re
from pymongo import MongoClient
from nltk import word_tokenize, sent_tokenize
from settings import *


client = MongoClient()
db = client[MONGO_DB]
enriched_collection = db[MONGO_COLLECTION_ENRICHED]

label = json.load(open(LABELED_DATA_PATH))

for entry in label:

    url = entry["source"]
    article = enriched_collection.find_one({"url": url})

    content = article["cleaned_content"]

    sentences = sent_tokenize(content)

    for entity in entry["talker"]:

        entity_key = entity["entity"].lower()

        print("entity_key\n====")
        if entity["correct"]:

            for sentence in sentences:

                for match in re.finditer(entity_key, sentence):
                    span = match.span()
                    begin_match, end_match = span

                    len_sentence = len(sentence)

                    begin = abs(begin_match - 20)
                    end = end_match + 20

                    if end > len_sentence:
                        end = len_sentence

                    print(sentence[begin:end])

        print("====")
