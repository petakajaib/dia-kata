from gensim.models.fasttext import FastText


def entity_generator(collection):
    for article in collection.find():
        yield article["entities"]


def build_fast_text_model(
        fasttext_entity_path,
        entity_collection):

    fasttext_params = {
        "hs": 1,
        "window": 10,
        "min_count": 1,
        "workers": 7,
        "min_n": 1,
        "max_n": 10,
    }

    print("building corpus")

    entity_corpus = [entity for entity in entity_generator(entity_collection)]
    fasttext_entity = FastText(**fasttext_params)

    print("count corpus")
    fasttext_entity.build_vocab(sentences=entity_corpus)
    total_examples = fasttext_entity.corpus_count

    print("train fasttext")
    fasttext_entity.train(
            sentences=entity_corpus,
            total_examples=total_examples,
            epochs=5)

    print("saving fasttext")

    fasttext_entity.save(fasttext_entity_path)

    return fasttext_entity
