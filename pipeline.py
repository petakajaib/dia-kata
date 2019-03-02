from pymongo import MongoClient
from preprocessing import add_content_to_label
from vectorization import vectorize_data
from modelling import modelling
from settings import *

client = MongoClient()
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

print("preprocessing")

# add_content_to_label(LABELED_DATA_PATH, PREPROCESSED_PATH, collection)

print("vectorization")

vectorize_data(PREPROCESSED_PATH, VECTORIZED_PATH)


print("modelling")

modelling(VECTORIZED_PATH)
