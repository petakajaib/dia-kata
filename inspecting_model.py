import json
import pickle
from pymongo import MongoClient
from gensim.models.fasttext import FastText
from sklearn.utils.validation import column_or_1d
from settings import *
from clustering import clustering
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

entities_counts = {"correct": [], "wrong": []}

talker_entities = []

for entry in labelled_data:

    entities = [entity["entity"] for entity in entry["talker"]]

    talker_entities.append(entities)


for idx, entry in enumerate(labelled_data):
    article = enriched_collection.find_one({"url": entry["source"]})


    feature_vector = vectorize_feature(entry, fast_text_models, enriched_collection)
    target_vector = vectorize_target(entry)

    target_vector_reshaped = column_or_1d(target_vector)

    predictions = clf.predict(feature_vector)

    correctness = evaluate_single_extraction(predictions, target_vector_reshaped, idx, talker_entities)

    all_entities = [entity["entity"] for entity in entry["talker"]]
    print("idx", idx)
    print("quote\n", entry["quote"])
    print("url", entry["source"])
    # print("url_count", url_map_count[entry["source"]])
    print("all_entities", all_entities)
    cluster_map = clustering(all_entities)
    print("cluster_map", cluster_map)
    inverse_cluster_map = {}

    for key, value in cluster_map.items():
        if not inverse_cluster_map.get(value):
            inverse_cluster_map[value] = set()

        inverse_cluster_map[value].add(key)
    if correctness == 0:
        print("wrong:")

        url_counts["wrong"].append(url_map_count[entry["source"]])
        # print("feature_vector\n", feature_vector)

        # print(json.dumps([entry["talker"][i]["entity"] for i, p in enumerate(predictions) if p == 1], indent=4))



        predictions_set = set()

        for i, pred_talker in enumerate(zip(predictions, entry["talker"])):

            prediction, entity_ = pred_talker
            entity = entity_["entity"]

            if prediction == 1.0:

                if cluster_map[entity] > -1:

                    predictions_set = predictions_set.union(inverse_cluster_map[cluster_map[entity]])
                else:
                    predictions_set.add(entity)

        print("prediction")
        print(json.dumps(list(predictions_set), indent=4))

        print("truth")
        print(json.dumps([entry["talker"][i]["entity"] for i, p in enumerate(target_vector_reshaped) if p==1], indent=4))

        entities_counts["wrong"].append(len(all_entities))
    elif correctness == 1:
        print("correct")
        url_counts["correct"].append(url_map_count[entry["source"]])
        entities_counts["correct"].append(len(all_entities))

        predictions_set = set()

        for i, pred_talker in enumerate(zip(predictions, entry["talker"])):

            prediction, entity_ = pred_talker
            entity = entity_["entity"]

            if prediction == 1.0:

                if cluster_map[entity] > -1:

                    predictions_set = predictions_set.union(inverse_cluster_map[cluster_map[entity]])
                else:
                    predictions_set.add(entity)

        print("prediction")
        print(json.dumps(list(predictions_set), indent=4))

        print("truth")
        print(json.dumps([entry["talker"][i]["entity"] for i, p in enumerate(target_vector_reshaped) if p==1], indent=4))


    print("---")


print("average wrong url_count:", sum(url_counts["wrong"])/len(url_counts["wrong"]))
print("median wrong url_count:", sorted(url_counts["wrong"])[int(len(url_counts["wrong"])/2)])
print("max wrong url_count:", max(url_counts["wrong"]))

print("average correct url_count:", sum(url_counts["correct"])/len(url_counts["correct"]))
print("median correct url_count:", sorted(url_counts["correct"])[int(len(url_counts["correct"])/2)])
print("max correct url_count:", max(url_counts["correct"]))

print("avg entities count for correct predictions", sum(entities_counts["correct"])/len(entities_counts["correct"]))
print("median entities count for correct predictions", sorted(entities_counts["correct"])[int(len(entities_counts["correct"])/2)])
print("max entities count for correct predictions", max(entities_counts["correct"]))

print("avg entities count for wrong predictions", sum(entities_counts["wrong"])/len(entities_counts["wrong"]))
print("median entities count for wrong predictions", sorted(entities_counts["wrong"])[int(len(entities_counts["wrong"])/2)])
print("max entities count for wrong predictions", max(entities_counts["wrong"]))
