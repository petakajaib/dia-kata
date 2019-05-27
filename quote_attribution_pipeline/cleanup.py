
def remove_duplicated_quotes(quote_collection):

    quote_ids = []

    for quote in quote_collection.distinct("quote"):

        entry = quote_collection.find_one({"quote": quote})
        quote_ids.append(entry["_id"])

    quote_collection.delete_many({"_id": {"$nin": quote_ids}})
