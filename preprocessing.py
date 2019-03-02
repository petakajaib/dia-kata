import json
import re

def add_content(entry, collection):

    article = collection.find_one({"url": entry["source"], "content": {"$exists":True}})

    if article:

        entry["content"] = article["content"]

    return entry

def get_cleaned_content(content):

    content = content.replace('“', "\"")
    content = content.replace('”', "\"")
    content = content.replace("‘", "'")
    # content = content.replace("\n", " ")
    content = content.replace("’", "'")
    content = content.replace("…", ".")
    content = re.sub("\s+", " ", content)

    return content

def add_cleaned_content(entry):

    entry["cleaned_content"] = get_cleaned_content(entry["content"])

    return entry

def add_content_to_label(labelling_source, labelling_target, collection, add_clean_content=True):
    labeled_data = json.load(open(labelling_source))
    added_content = []

    for entry in labeled_data:

        entry = add_content(entry, collection)
        entry = add_cleaned_content(entry)
        entry["quote"] = get_cleaned_content(entry["quote"])
        added_content.append(entry)
        print(json.dumps(entry, indent=4))

    json.dump(added_content, open(labelling_target, "w"))
    return added_content
