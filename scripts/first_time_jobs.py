from datetime import datetime, timedelta
import pickle
from annoy import AnnoyIndex
from gensim.models.fasttext import FastText
from gensim.summarization.keywords import keywords as get_keywords
from polyglot.text import Text
import pycld2
from pymongo import MongoClient
from settings import (
    MONGO_DB,
    MONGO_COLLECTION,
    ENTITY_COLLECTION,
    ANNOY_INDEX_COLLECTION,
    QUOTE_COLLECTION,
    MONGO_COLLECTION_ENRICHED,
    SIMILAR_ENTITIES_COLLECTION,
    ENTITY_KEYWORDS_COLLECTION,
    FASTTEXT_ENGLISH,
    FASTTEXT_MALAY,
    CURRENT_BEST_MODEL,
    FASTTEXT_ENTITY,
    ANNOY_INDEX_PATH
)
from extraction_pipeline import extract_quote_talkers


def entity_generator(collection):
    for article in collection.find():
        yield article["entities"]


def populate_entity_collection(
        article_collection,
        entity_collection):

    entity_urls = entity_collection.distinct("url", {})

    article_collection.update_many(
        {"done_entity_population": {"$exists": False}},
        {"$set": {"done_entity_population": False}}
    )

    query = {
        # "publish_date": {"$gte": datetime(2019,4,5)},
        "content": {"$exists": True},
        "url": {"$nin": entity_urls},
        "done_entity_population": False
    }

    total_count = article_collection.count(query)

    for idx, article in enumerate(article_collection.find(
            query, no_cursor_timeout=True)):

        print("{} of {} url: {}".format(idx, total_count, article["url"]))

        try:
            parsed = Text(article["content"])
            entities = [" ".join(entity).lower() for entity in parsed.entities]

            entity = {
                "entities": entities,
                "url": article["url"],
                "detected_language": parsed.detect_language(),
                "publish_date": article["publish_date"]
            }

            entity_collection.insert_one(entity)

        except pycld2.error as err:
            print(err)
        except ValueError as err:
            print(err)

        article_collection.update_one(
            {"_id": article["_id"]},
            {"$set": {"done_entity_population": True}}
        )


def build_fast_text_model(fasttext_entity_path):
    # build fastText

    fasttext_params = {
        "hs": 1,
        "window": 10,
        "min_count": 1,
        "workers": 7,
        "min_n": 1,
        "max_n": 10,
    }

    print("building corpus")

    entity_corpus = [entity for entity in entity_generator(entity_collection)]
    fasttext_entity = FastText(**fasttext_params)

    print("count corpus")
    fasttext_entity.build_vocab(sentences=entity_corpus)
    total_examples = fasttext_entity.corpus_count

    print("train fasttext")
    fasttext_entity.train(sentences=entity_corpus, total_examples=total_examples, epochs=5)

    print("saving fasttext")

    fasttext_entity.save(fasttext_entity_path)

    return fasttext_entity


def add_to_annoy_index(entity, annoy_index_collection, fasttext_entity, annoy_index):

    annoy_index_collection.insert_one({
        "idx": idx,
        "entity": entity
        })

    vector = fasttext_entity[entity]

    annoy_index.add_item(idx, vector)


def build_annoy_index(collection, annoy_index_collection,
                      fasttext_entity, dimension, annoy_index_path):

    annoy_index = AnnoyIndex(dimension)

    annoy_index_collection.delete_many({})

    for idx, entity in enumerate(collection.distinct("talker", {})):

        if annoy_index_collection.count({"entity": entity}) == 0:
            annoy_index_collection.insert_one({
                "idx": idx,
                "entity": entity
                })

            vector = fasttext_entity[entity]

            annoy_index.add_item(idx, vector)

    annoy_index.build(10)
    annoy_index.save(annoy_index_path)

    return annoy_index


def batch_quote_extraction(
        quote_model_path,
        article_collection,
        enriched_collection,
        quote_collection,
        fast_text_models):

    print("loading quote model")

    quote_model = pickle.load(open(quote_model_path, "rb"))

    quote_query = {
        "detected_language": {"$in": ["ms", "en"]},
        "content": {"$exists": True},
        "done_quote_extraction": False
    }

    article_collection.update_many(
        {"done_quote_extraction": {"$exists": False}},
        {"$set": {"done_quote_extraction": False}}
    )

    total_count = article_collection.count(quote_query)

    for idx, article in enumerate(article_collection.find(
            quote_query, no_cursor_timeout=True)):

        print("{} of {}. url: {}".format(idx, total_count, article["url"]))
        try:
            quote_talkers = extract_quote_talkers(
                article, enriched_collection,
                fast_text_models, quote_model)
        except KeyError as err:
            print(err)
            continue
        except ValueError as err:
            print(err)
            continue

        d = {
            "url": article["url"],
            "detected_language": article["detected_language"],
            "publish_time": article["publish_time"]
        }

        for quote_talker in quote_talkers:

            quote_entry = {**d, **quote_talker}

            try:
                parsed_quote = Text(quote_entry["quote"])
                mentions = [" ".join(t).lower() for t in parsed_quote.entities if t.tag == "I-PER"]
            except pycld2.error as err:
                print(err)
                mentions = []
            except ValueError as err:
                print(err)
                mentions = []

            quote_entry["mentions"] = mentions

            quote_collection.insert_one(quote_entry)

        article_collection.update_one(
            {"_id": article["_id"]},
            {"$set": {"done_quote_extraction": True}}
            )


def get_similar_entities(
        query, fasttext_entity,
        annoy_index, annoy_index_collection,
        n_results=10):

    vector = fasttext_entity[query]

    aggregated = []
    for result in annoy_index.get_nns_by_vector(vector, 500):

        res = annoy_index_collection.find_one({"idx": result})

        query_set = set(query.lower().split())
        entity_set = set(res["entity"].split())

        if query in res["entity"]:
            continue
        if len(query_set.intersection(entity_set)):
            continue
        else:
            aggregated.append(res["entity"])

    return aggregated[:n_results]


if __name__ == '__main__':

    client = MongoClient()

    db = client[MONGO_DB]
    article_collection = db[MONGO_COLLECTION]
    entity_collection = db[ENTITY_COLLECTION]
    annoy_index_collection = db[ANNOY_INDEX_COLLECTION]
    quote_collection = db[QUOTE_COLLECTION]
    enriched_collection = db[MONGO_COLLECTION_ENRICHED]
    similar_entities_collection = db[SIMILAR_ENTITIES_COLLECTION]
    entity_keywords_collection = db[ENTITY_KEYWORDS_COLLECTION]

    print("loading FastText models")

    print("en")
    en_fasttext = FastText.load(FASTTEXT_ENGLISH, mmap='r')
    print("ms")
    ms_fasttext = FastText.load(FASTTEXT_MALAY, mmap='r')

    fast_text_models = {
        "en": en_fasttext,
        "ms": ms_fasttext
    }

    batch_quote_extraction(
            CURRENT_BEST_MODEL,
            article_collection,
            enriched_collection,
            quote_collection,
            fast_text_models
            )

    print("populate_entity_collection")

    populate_entity_collection(article_collection, entity_collection)

    print("load FastText entity")

    # print("build_fast_text_model")
    # build_fast_text_model(FASTTEXT_ENTITY)
    fasttext_entity = FastText.load(FASTTEXT_ENTITY)

    print("build_annoy_index entities")

    dimension = 100

    annoy_index = build_annoy_index(
        quote_collection, annoy_index_collection,
        fasttext_entity, dimension, ANNOY_INDEX_PATH)

    annoy_index = AnnoyIndex(dimension)
    annoy_index.load(ANNOY_INDEX_PATH)


    dummy_created_at = datetime(2019,4,20)
    query_date = datetime(
        dummy_created_at.year,
        dummy_created_at.month,
        dummy_created_at.day
        )
    print("populate similar entities")

    talkers = quote_collection.distinct("talker", {})
    count_talkers = len(talkers)

    for idx, talker in enumerate(talkers):

        if similar_entities_collection.count({
            "entity": talker,
            "created_at": {
                "$gte": query_date,
                "$lt": query_date + timedelta(days=1)
                }
            }) > 0:

            continue

        print("populate similar entities {} of {}. entity: {}".format(
            idx,
            count_talkers,
            talker
        ))
        similar_entities = get_similar_entities(
            talker, fasttext_entity,
            annoy_index, annoy_index_collection,
            )

        similar_entry = {
            "entity": talker,
            "similar": similar_entities,
            "created_at": dummy_created_at
        }
        similar_entities_collection.insert_one(similar_entry)


    print("populate keywords")

    for idx, talker in enumerate(talkers):

        if entity_keywords_collection.count({
            "entity": talker,
            "created_at": {
                "$gte": query_date,
                "$lt": query_date + timedelta(days=1)
                }
            }) > 0:

            continue

        print("populate keywords {} of {}. entity: {}".format(
            idx,
            count_talkers,
            talker
        ))

        urls = quote_collection.distinct("url", {"talker": talker})

        contents = [a["content"] for a in article_collection.find({"url": {"$in": urls}}).sort("publish_time", -1)]

        blob = " ".join(contents[:100])

        keywords = get_keywords(blob, split=True)

        keywords_entry = {
            "entity": talker,
            "keywords": keywords,
            "created_at": dummy_created_at
        }

        entity_keywords_collection.insert_one(keywords_entry)
