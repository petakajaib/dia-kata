import json
from pymongo import MongoClient
from settings import *
from polyglot.text import Text

def add_content(entry, collection):

    article = collection.find_one({"url": entry["source"], "content": {"$exists":True}})

    if article:

        entry["content"] = article["content"]

    return entry

def add_content_to_label(labelling_source, labelling_target, collection):
    labeled_data = json.load(open(labelling_source))
    added_content = []

    for entry in labeled_data:

        entry = add_content(entry, collection)
        added_content.append(entry)
        print(json.dumps(entry, indent=4))

    json.dump(added_content, open(labelling_target, "w"))
    return added_content



client = MongoClient()
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

labelled_data_path = "data/labelled_data_with_content.json"

labelled_data = json.load(open(labelled_data_path))

for entry in labelled_data:

    print(entry)

    content = entry["content"]

    parsed = Text(content)

    tokens = parsed.tokens

    tokens_normalized = [str(token) for token in tokens]
