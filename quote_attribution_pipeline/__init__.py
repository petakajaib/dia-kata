from datetime import datetime
from annoy import AnnoyIndex
from gensim.models.fasttext import FastText
from pymongo import MongoClient
from .build_fasttext_entity import build_fast_text_model
from .quote_extraction import batch_quote_extraction
from .populate_entities import populate_entity_collection
from .similarity_index import (
    populate_similar_entities,
    get_similar_entities,
    build_annoy_index)
from .keywords_extraction import populate_keywords
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


def quote_attribution(logger=None, query_date=None):

    if query_date is None:
        n = datetime.now()
        query_date = datetime(n.year, n.month, n.day)

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
    if logger:
        logger.info("loading FastText models")

    with open("logs/api.log", "a") as f:
        f.write("loading FastText models")

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

    print("build_fast_text_model")
    build_fast_text_model(FASTTEXT_ENTITY, entity_collection)
    fasttext_entity = FastText.load(FASTTEXT_ENTITY)

    print("build_annoy_index entities")

    dimension = 100

    annoy_index = build_annoy_index(
        quote_collection, annoy_index_collection,
        fasttext_entity, dimension, ANNOY_INDEX_PATH)

    annoy_index = AnnoyIndex(dimension)
    annoy_index.load(ANNOY_INDEX_PATH)
    talkers = quote_collection.distinct("talker", {})

    print("populate similar entities")

    populate_similar_entities(
        talkers,
        query_date,
        fasttext_entity,
        annoy_index,
        quote_collection,
        similar_entities_collection,
        annoy_index_collection
        )

    print("populate keywords")

    populate_keywords(
        talkers,
        entity_keywords_collection,
        query_date,
        quote_collection,
        article_collection)
