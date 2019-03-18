import json
import pycld2
from pprint import pprint
from polyglot.text import Text
from pymongo import MongoClient
from preprocessing import get_cleaned_content
from settings import *

def parse_text(label, text):

    parsed = Text(text)

    try:
        tokens = [str(token) for token in parsed.tokens]
    except pycld2.error as err:
        tokens = [token for token in text.split(" ")]

    try:
        sentences = [str(sentence) for sentence in parsed.sentences]
    except pycld2.error as err:
        sentences = text.split(".")

    entities = []
    entities_parsed = {}
    entities_tag = {}

    try:
        for entity in parsed.entities:

            combined_ent = [str(ent).lower() for ent in entity]

            joined = " ".join(combined_ent).replace(".", "DOT")
            entities.append(joined)
            entities_parsed[joined] = combined_ent
            entities_tag[joined] = entity.tag
    except ValueError as err:
        print(err)
    except pycld2.error as err:
        print(err)

    d = {}
    d[label] = text
    d["{}_tokens".format(label)] = tokens
    d["{}_sentences".format(label)] = sentences
    d["{}_entities".format(label)] = entities
    d["{}_entities_parsed".format(label)] = entities_parsed
    d["{}_entities_tag".format(label)] = entities_tag

    return d

def insert_to_enriched_collection(article, enriched_collection):
    if enriched_collection.count({"url": article["url"]}) == 0:
        entry = {}
        entry["url"] = article["url"]
        entry["language"] = article["detected_language"]
        title = article["title"]
        content = article["content"]

        cleaned_title = get_cleaned_content(title)
        cleaned_content = get_cleaned_content(content)

        text_forms = [
            ("cleaned_content", cleaned_content),
            ("lowered_content", cleaned_content.lower()),
            ("title", title),
            ("cleaned_title", cleaned_title),
            ("lowered_title", cleaned_title.lower())
        ]

        for label, text in text_forms:
            parsed = parse_text(label, text)

            for key, value in parsed.items():
                entry[key] = value

        enriched_collection.insert_one(entry)
        return entry
    else:
        return enriched_collection.find_one({"url": article["url"]})

if __name__ == '__main__':

    client = MongoClient()
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    enriched_collection = db[MONGO_COLLECTION_ENRICHED]

    labelled_data = json.load(open(LABELED_DATA_PATH))

    distinct_urls = set([entry["source"] for entry in labelled_data])

    for url in distinct_urls:
        print(url)

        article = collection.find_one({"url": url})

        entry = insert_to_enriched_collection(article, enriched_collection)
        print(entry)
