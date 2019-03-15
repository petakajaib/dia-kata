import json
import pickle
from pprint import pprint
from pymongo import MongoClient
from gensim.models.fasttext import FastText
from sklearn.utils.validation import column_or_1d
from settings import *
from clustering import clustering
from vectorize import vectorize_feature, vectorize_target
from model import evaluate_single_extraction
from talker_candidate import (
    get_talker_candidates,
    filter_candidates_by_heuristics
    )

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
    entity_tags = article["cleaned_content_entities_tag"]

    feature_vector = vectorize_feature(entry, fast_text_models, enriched_collection)
    target_vector = vectorize_target(entry)

    target_vector_reshaped = column_or_1d(target_vector)

    predictions = clf.predict(feature_vector)

    predictions_prob = clf.predict_proba(feature_vector)

    correctness = evaluate_single_extraction(predictions, target_vector_reshaped, idx, talker_entities)

    all_entities = [entity["entity"] for entity in entry["talker"]]
    # print("idx", idx)
    print("quote", entry["quote"])
    print("url", entry["source"])

    # print("all_entities", all_entities)
    cluster_map, inverse_cluster_map = clustering(all_entities, return_inverse=True)
    print("cluster_map", cluster_map)
    if correctness == 0:
        pass
        # print("wrong:")
        #
        # url_counts["wrong"].append(url_map_count[entry["source"]])
        # entities_counts["wrong"].append(len(all_entities))
        #
        # print("prediction")
        # talker_candidates = get_talker_candidates(predictions_prob, all_entities, cluster_map, inverse_cluster_map)
        # pprint(talker_candidates)
        #
        # print("truth")
        # pprint([entry["talker"][i]["entity"] for i, p in enumerate(target_vector_reshaped) if p==1])
        #
        # entities_counts["wrong"].append(len(all_entities))
    elif correctness == 1:
        print("correct:")
        url_counts["correct"].append(url_map_count[entry["source"]])
        entities_counts["correct"].append(len(all_entities))

        print("prediction")
        talker_candidates_prob = get_talker_candidates(predictions_prob, all_entities, cluster_map, inverse_cluster_map, return_prob)
        # pprint(talker_candidates)
        talker_candidates = []
        talker_prob_map = {}

        for talker, prob in talker_candidates_prob:
            talker_candidates.append(talker)
            talker_prob_map[talker] = prob

        filtered_condidates = filter_candidates_by_heuristics(talker_candidates, entity_tags)
        print([(entity, talker_prob_map[entity])for entity in filtered_condidates
        
        print("truth")
        pprint([entry["talker"][i]["entity"] for i, p in enumerate(target_vector_reshaped) if p==1])


    print("---")


# print("average wrong url_count:", sum(url_counts["wrong"])/len(url_counts["wrong"]))
# print("median wrong url_count:", sorted(url_counts["wrong"])[int(len(url_counts["wrong"])/2)])
# print("max wrong url_count:", max(url_counts["wrong"]))

print("average correct url_count:", sum(url_counts["correct"])/len(url_counts["correct"]))
print("median correct url_count:", sorted(url_counts["correct"])[int(len(url_counts["correct"])/2)])
print("max correct url_count:", max(url_counts["correct"]))

print("avg entities count for correct predictions", sum(entities_counts["correct"])/len(entities_counts["correct"]))
print("median entities count for correct predictions", sorted(entities_counts["correct"])[int(len(entities_counts["correct"])/2)])
print("max entities count for correct predictions", max(entities_counts["correct"]))

# print("avg entities count for wrong predictions", sum(entities_counts["wrong"])/len(entities_counts["wrong"]))
# print("median entities count for wrong predictions", sorted(entities_counts["wrong"])[int(len(entities_counts["wrong"])/2)])
# print("max entities count for wrong predictions", max(entities_counts["wrong"]))
