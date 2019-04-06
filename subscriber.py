# entity extraction

# quote extraction and attribution
if entity_collection.count({"url": article["url"]}) == 0:

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
        continue

insert_to_enriched_collection(article, enriched_collection)

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

pipeline = [{"$match": {"content": {"$exists": True}, "detected_language": {"$in":["en", "ms"]}}}, {"$sample": {"size":10000}}]

for article in article_collection.aggregate(pipeline):
    print(article["url"])
    quote_talkers = extract_quote_talkers(article, enriched_collection, fast_text_models, quote_model)

    pprint(quote_talkers)
