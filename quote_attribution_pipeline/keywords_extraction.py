from datetime import timedelta
from gensim.summarization.keywords import keywords as get_keywords


def get_keywords_entry(
        query_date,
        talker,
        quote_collection,
        article_collection
        ):

    urls = quote_collection.distinct("url", {"talker": talker})

    contents = [a["content"] for a in article_collection.find(
                {"url": {"$in": urls}}).sort("publish_time", -1)]

    blob = " ".join(contents[:100])

    keywords = get_keywords(blob, split=True)

    return {
        "entity": talker,
        "keywords": keywords,
        "created_at": query_date
    }


def populate_keywords(
        talkers,
        entity_keywords_collection,
        query_date,
        quote_collection,
        article_collection):

    count_talkers = len(talkers)

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

        keywords_entry = get_keywords_entry(
                            query_date,
                            talker,
                            quote_collection,
                            article_collection
                            )

        entity_keywords_collection.insert_one(keywords_entry)
