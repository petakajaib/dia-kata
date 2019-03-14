import json
import pickle
from pymongo import MongoClient
from gensim.models.fasttext import FastText
from sklearn.utils.validation import column_or_1d
from settings import *
from vectorize import vectorize_feature, vectorize_target
from model import evaluate_single_extraction


client = MongoClient()

db = client[MONGO_DB]

enriched_collection = db[MONGO_COLLECTION_ENRICHED]


print("loading fasttext models")
print("en")
en_fasttext = FastText.load(FASTTEXT_ENGLISH, mmap='r')

print("ms")
ms_fasttext = FastText.load(FASTTEXT_MALAY, mmap='r')
print("fasttext models loaded")

fast_text_models = {
    "en": en_fasttext,
    "ms": ms_fasttext
}

url_map_count = {}


labelled_data = json.load(open(PREPROCESSED_PATH))

for entry in labelled_data:

    if not url_map_count.get(entry["source"]):
        url_map_count[entry["source"]] = 0

    url_map_count[entry["source"]] += 1



clf = pickle.load(open(CURRENT_BEST_MODEL, "rb"))

url_counts = {"correct": [], "wrong":[]}

for idx, entry in enumerate(labelled_data):
    article = enriched_collection.find_one({"url": entry["source"]})


    feature_vector = vectorize_feature(entry, fast_text_models, enriched_collection)
    target_vector = vectorize_target(entry)

    target_vector_reshaped = column_or_1d(target_vector)

    predictions = clf.predict(feature_vector)
:
    entities = [entity["entity"] for entity in entry["talker"]]
    correctness = evaluate_single_extraction(predictions, target_vector_reshaped, idx, entities)

    if correctness == 0:

        print("idx", idx)
        print("quote\n", entry["quote"])
        print("url", entry["source"])
        # print("url_count", url_map_count[entry["source"]])
        all_entities = article["cleaned_content_entities"]
        print("all_entities", all_entities)
        url_counts["wrong"].append(url_map_count[entry["source"]])
        # print("feature_vector\n", feature_vector)
        print("prediction")

        print(json.dumps([entry["talker"][i]["entity"] for i, p in enumerate(predictions) if p == 1], indent=4))

        print("truth")

        print(json.dumps([entry["talker"][i]["entity"] for i, p in enumerate(target_vector_reshaped) if p==1], indent=4))
        print("---")
    elif correctness == 1:
        url_counts["correct"].append(url_map_count[entry["source"]])

print("average wrong url_count:", sum(url_counts["wrong"])/len(url_counts["wrong"]))
print("median wrong url_count:", sorted(url_counts["wrong"])[int(len(url_counts["wrong"])/2)])
print("max wrong url_count:", max(url_counts["wrong"]))

print("average correct url_count:", sum(url_counts["correct"])/len(url_counts["correct"]))
print("median correct url_count:", sorted(url_counts["correct"])[int(len(url_counts["correct"])/2)])
print("max correct url_count:", max(url_counts["correct"]))
