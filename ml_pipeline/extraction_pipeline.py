import pickle
from pprint import pprint
import re
from pymongo import MongoClient
import pycld2
from gensim.models.fasttext import FastText
from .labelled_data_enrichments import insert_to_enriched_collection
from polyglot.text import Text
from .clustering import clustering
from .preprocessing import get_cleaned_content
from .vectorize import vectorize_feature
from .talker_candidate import (
    get_talker_candidates,
    select_candidate
    )
from settings import (
    MONGO_DB,
    MONGO_COLLECTION,
    MONGO_COLLECTION_ENRICHED,
    FASTTEXT_ENGLISH,
    FASTTEXT_MALAY,
    CURRENT_BEST_MODEL
)


def quoted_text_generator(article, length_min_threshold=5,
                          length_max_threshold=45,
                          left_padding=50,
                          right_padding=70):

    content = get_cleaned_content(article["content"])
    for quoted_text in re.findall(
            r'"([A-Za-z0-9_\./\\ -]+)"',
            content, re.MULTILINE):

        text_length = len(quoted_text.split())

        if length_min_threshold <= text_length <= length_max_threshold:

            if quoted_text[0] == " ":
                continue

            yield quoted_text


def get_entities(text):

    try:
        parsed = Text(text)

        return [{"entity": " ".join(ent).title()} for ent in parsed.entities]
    except pycld2.error as err:
        print(err)
        return []

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


def extract_quote_talkers(article, enriched_collection,
                          fast_text_models, quote_model):

    quote_talkers = []

    insert_to_enriched_collection(article, enriched_collection)
    enriched = enriched_collection.find_one({"url": article["url"]})
    all_entities = enriched["cleaned_content_entities"]
    entity_tags = enriched["cleaned_content_entities_tag"]
    for entry in entry_generator(article):
        try:
            feature_vector = vectorize_feature(
                    entry, fast_text_models,
                    enriched_collection)

            predictions_prob = quote_model.predict_proba(feature_vector)
            cluster_map, inverse_cluster_map = clustering(
                    all_entities,
                    return_inverse=True)

            talker_candidates = get_talker_candidates(
                    predictions_prob, all_entities,
                    cluster_map, inverse_cluster_map)

            selected = select_candidate(
                    talker_candidates,
                    entity_tags)

            if selected:
                d = {
                    "quote": entry["quote"],
                    "talker": selected
                }
                quote_talkers.append(d)
        except TypeError as err:
            print(err)
    return quote_talkers


if __name__ == '__main__':

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

    print("loading quote model")

    quote_model = pickle.load(open(CURRENT_BEST_MODEL, "rb"))
    query = {
        "content": {"$exists": True},
        "detected_language": {"$in": ["en", "ms"]}
    }

    pipeline = [{"$match": query}, {"$sample": {"size": 10000}}]

    for article in article_collection.aggregate(pipeline):
        print(article["url"])

        quote_talkers = extract_quote_talkers(
            article, enriched_collection,
            fast_text_models, quote_model)

        pprint(quote_talkers)
