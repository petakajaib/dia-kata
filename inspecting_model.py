import json
import pickle
from pymongo import MongoClient
from gensim.models.fasttext import FastText
from sklearn.utils.validation import column_or_1d
from settings import *
from vectorize import vectorize_feature, vectorize_target



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

labelled_data = json.load(open(PREPROCESSED_PATH))

clf = pickle.load(open(CURRENT_BEST_MODEL, "rb"))

for idx, entry in enumerate(labelled_data):
    print("idx", idx)
    print("quote\n", entry["quote"])
    feature_vector = vectorize_feature(entry, fast_text_models, enriched_collection)
    target_vector = vectorize_target(entry)

    target_vector_reshaped = column_or_1d(target_vector)

    predictions = clf.predict(feature_vector)

    for entity, truth, prediction in zip(entry["talker"], target_vector_reshaped, predictions):

        if truth == 1:
            print("entity", entity["entity"])

            if prediction == 0:
                print("did not extract when should extract")
            elif prediction == 1:
                print("extracted correctly")

        if truth == 0 and prediction == 1:
            print("entity", entity["entity"])
            print("extracted wrongly")

    print("prediction")

    print(json.dumps([entry["talker"][i]["entity"] for i, p in enumerate(predictions) if p == 1], indent=4))

    print("truth")

    print(json.dumps([entry["talker"][i]["entity"] for i, p in enumerate(target_vector_reshaped) if p==1], indent=4))
    print("---")
