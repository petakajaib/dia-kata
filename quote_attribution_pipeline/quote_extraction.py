import pickle
from polyglot.text import Text
import pycld2
from ml_pipeline import extract_quote_talkers


def get_quote_entry(
        article_attributes,
        quote_talker):
    quote_entry = {**article_attributes, **quote_talker}

    try:
        parsed_quote = Text(quote_entry["quote"])
        mentions = [" ".join(t).lower() for t in
                    parsed_quote.entities
                    if t.tag == "I-PER"]
    except pycld2.error as err:
        print(err)
        mentions = []
    except ValueError as err:
        print(err)
        mentions = []

    quote_entry["mentions"] = mentions

    return quote_entry


def quote_extraction(
            article, enriched_collection,
            fast_text_models, quote_model,
            quote_collection, article_collection):

    try:
        quote_talkers = extract_quote_talkers(
            article, enriched_collection,
            fast_text_models, quote_model)
        d = {
            "url": article["url"],
            "detected_language": article["detected_language"],
            "publish_time": article["publish_time"]
        }

        for quote_talker in quote_talkers:

            quote_entry = get_quote_entry(d, quote_talker)

            quote_collection.insert_one(quote_entry)

            article_collection.update_one(
                {"_id": article["_id"]},
                {"$set": {"done_quote_extraction": True}}
                )
    except KeyError as err:
        print(err)
    except ValueError as err:
        print(err)


def batch_quote_extraction(
        quote_model_path,
        article_collection,
        enriched_collection,
        quote_collection,
        fast_text_models):

    print("loading quote model")

    quote_model = pickle.load(open(quote_model_path, "rb"))

    article_collection.update_many(
        {"done_quote_extraction": {"$exists": False}},
        {"$set": {"done_quote_extraction": False}}
    )

    quote_query = {
        "detected_language": {"$in": ["ms", "en"]},
        "content": {"$exists": True},
        "done_quote_extraction": False
    }

    total_count = article_collection.count(quote_query)

    for idx, article in enumerate(article_collection.find(
            quote_query, no_cursor_timeout=True)):

        print("{} of {}. url: {}".format(idx, total_count, article["url"]))
        quote_extraction(
            article, enriched_collection,
            fast_text_models, quote_model,
            quote_collection, article_collection)
