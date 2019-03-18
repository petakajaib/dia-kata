import pickle
import re
from pymongo import MongoClient
from gensim.models.fasttext import FastText
from labelled_data_enrichments import insert_to_enriched_collection
from polyglot.text import Text
from clustering import clustering
from preprocessing import get_cleaned_content
from vectorize import vectorize_feature
from talker_candidate import (
    get_talker_candidates,
    select_candidate
    )
from settings import *

def quoted_text_generator(article, length_min_threshold=5, length_max_threshold=45, left_padding=50, right_padding=70):

    content = get_cleaned_content(article["content"])
    for quoted_text in re.findall(r'"([A-Za-z0-9_\./\\ -]+)"', content, re.MULTILINE):

        text_length = len(quoted_text.split())

        if length_min_threshold <= text_length <= length_max_threshold:

            if quoted_text[0] == " ":
                continue

            idx = content.find(quoted_text)
            quoted_text_char_length = len(quoted_text)

            yield quoted_text

def get_entities(text):

    parsed = Text(text)

    return [{"entity":" ".join(ent).title()} for ent in parsed.entities]

def transform_to_entry(article, quoted_text):

    cleaned_content = get_cleaned_content(article["content"])

    transformed = {
        "quote": quoted_text,
        "source": article["url"],
        "content": article["content"],
        "language": article["detected_language"],
        "cleaned_content": cleaned_content,
        "talker": get_entities(cleaned_content)
        }

    return transformed

def entry_generator(article):

    for quoted_text in quoted_text_generator(article):

        yield transform_to_entry(article, quoted_text)

client = MongoClient()
db = client[MONGO_DB]
article_collection = db[MONGO_COLLECTION]
enriched_collection = db[MONGO_COLLECTION_ENRICHED]


print("loading FastText models")

print("en")
en_fasttext = FastText.load(FASTTEXT_ENGLISH, mmap='r')

print("ms")
ms_fasttext = FastText.load(FASTTEXT_MALAY, mmap='r')

fast_text_models = {
    "en": en_fasttext,
    "ms": ms_fasttext
}

pipeline = [{"$match": {"content": {"$exists": True}, "detected_language": {"$in":["en", "ms"]}}}, {"$sample": {"size":10}}]


clf = pickle.load(open(CURRENT_BEST_MODEL, "rb"))

for article in article_collection.aggregate(pipeline):

    print("enrichment")

    insert_to_enriched_collection(article, enriched_collection)
    enriched = enriched_collection.find_one({"url": article["url"]})
    all_entities = entities["cleaned_content_entities"]
    entity_tags = entities["cleaned_content_entities_tag"]
    for entry in entry_generator(article):
        print("vectorize_feature")

        feature_vector = vectorize_feature(entry, fast_text_models, enriched_collection)
        print("prediction")
        predictions_prob = clf.predict_proba(feature_vector)
        cluster_map, inverse_cluster_map = clustering(all_entities, return_inverse=True)
        talker_candidates = get_talker_candidates(predictions_prob, all_entities, cluster_map, inverse_cluster_map)
        selected = select_candidate(talker_candidates, entity_tags)

        pritn(selected)
