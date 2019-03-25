MONGO_DB = "kronologi_malaysia"
MONGO_COLLECTION = "article"
PARSED_CLEANED_COLLECTION = "parsed_cleaned_sentences"
LABELLER_BASE_URL = "http://localhost:1337"
WIKIPEDIA_FASTTEXT_MS = "../fast_text_pretrained/wiki.ms.bin"
WIKIPEDIA_FASTTEXT_EN = "../fast_text_pretrained/wiki.en.bin"
X_MS_SENTIMENT = "../modelling_vectors/talking-bad-and-good/x_ms_sentiment.npy"
Y_MS_SENTIMENT = "../modelling_vectors/talking-bad-and-good/y_ms_sentiment.npy"
X_EN_SENTIMENT = "../modelling_vectors/talking-bad-and-good/x_en_sentiment.npy"
Y_EN_SENTIMENT = "../modelling_vectors/talking-bad-and-good/y_en_sentiment.npy"
X_MS_TALKER = "../modelling_vectors/talking-bad-and-good/x_ms_talker.npy"
Y_MS_TALKER = "../modelling_vectors/talking-bad-and-good/y_ms_talker.npy"
X_MS_TALKED_ABOUT = "../modelling_vectors/talking-bad-and-good/x_ms_talked_about.npy"
Y_MS_TALKED_ABOUT = "../modelling_vectors/talking-bad-and-good/y_ms_talked_about.npy"
X_EN_TALKER = "../modelling_vectors/talking-bad-and-good/x_en_talker.npy"
Y_EN_TALKER = "../modelling_vectors/talking-bad-and-good/y_en_talker.npy"
X_EN_TALKED_ABOUT = "../modelling_vectors/talking-bad-and-good/x_en_talked_about.npy"
Y_EN_TALKED_ABOUT = "../modelling_vectors/talking-bad-and-good/y_en_talked_about.npy"

# FASTTEXT_ENGLISH = "../fast_text_models/talking-bad-and-good-models/fasttext_english"
# FASTTEXT_MALAY = "../fast_text_models/talking-bad-and-good-models/fasttext_malay"

FASTTEXT_ENGLISH = "../fast_text_models/english_1_wiki_initialized"
FASTTEXT_MALAY = "../fast_text_models/lowered_stop_words_removed_wiki_initialized"

MALAY_STOPWORD = "malay_stopwords.txt"

SENTIMENT_MODEL_EN = "../xgboost-models/sentiment_en.pickle"
TALKED_ABOUT_MODEL_EN = "../xgboost-models/talked_about_en.pickle"
TALKER_MODEL_EN = "../xgboost-models/talker_en.pickle"

SENTIMENT_MODEL_MS = "../xgboost-models/sentiment_ms.pickle"
TALKED_ABOUT_MODEL_MS = "../xgboost-models/talked_about_ms.pickle"
TALKER_MODEL_MS = "../xgboost-models/talker_ms.pickle"


TALKING_COLLECTION = "talking"

ENTITY_EXTRACTION_COLLECTION = "entity_extraction"

SELECTED_TALKED_ABOUT_JSON = "data/selected_talked_about.json"
SELECTED_TALKER_JSON = "data/selected_talker.json"
CONTENT_ADDED_PATH = "data/labelled_data_with_content.json"
PREPROCESSED_PATH = "data/labelled_data_with_language.json"
VECTORIZED_PATH = "data/vectorized_data.pkl"
LABELED_DATA_PATH = "data/labelling.json"
MONGO_COLLECTION_ENRICHED = "enriched_for_extracting_talker"
SPEECH_VERB_PATH = "data/speech_verbs_uniq.txt"
CURRENT_BEST_MODEL = "data/model_with_anti_entity.pkl"
