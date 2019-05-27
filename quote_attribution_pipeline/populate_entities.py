from polyglot.text import Text
import pycld2


def get_entity(article):

    try:
        parsed = Text(article["content"])
        entities = [" ".join(entity).lower() for entity in parsed.entities]
    except pycld2.error as err:
        print(err)
        entities = []
        
    return {
        "entities": entities,
        "url": article["url"],
        "detected_language": parsed.detect_language(),
        "publish_date": article["publish_date"]
    }


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

            entity = get_entity(article)

            entity_collection.insert_one(entity)

        except pycld2.error as err:
            print(err)
        except ValueError as err:
            print(err)

        article_collection.update_one(
            {"_id": article["_id"]},
            {"$set": {"done_entity_population": True}}
        )
