import json
from settings import *

labelled_data = json.load(open(PREPROCESSED_PATH))

print(json.dumps(labelled_data, indent=4))
