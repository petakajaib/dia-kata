import json
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from settings import *

labelled_data = json.load(open(PREPROCESSED_PATH))

for label in labelled_data:

    for entity in label["talker"]:
        print(entity["entity"])
