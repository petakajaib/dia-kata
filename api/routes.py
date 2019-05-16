from flask import request, Response, jsonify
from gensim.models.fasttext import FastText
from annoy import AnnoyIndex
from .mongo_collections import (
    annoy_index_collection,
    entity_keywords_collection,
    quote_collection
)
# from .validators import validate
from .controllers import get_detail, get_search_results
from settings import (
    ANNOY_INDEX_PATH,
    FASTTEXT_ENTITY
)


dimension = 100

annoy_index = AnnoyIndex(dimension)
annoy_index.load(ANNOY_INDEX_PATH)
fasttext_entity = FastText.load(FASTTEXT_ENTITY)


def init_app(app):

    @app.route("/search/", methods=['POST'])
    def search():
        return get_search_results(
                    request, fasttext_entity,
                    annoy_index, annoy_index_collection)

    @app.route("/detail/", methods=['POST'])
    def detail():
        return get_detail(
                    request, quote_collection,
                    entity_keywords_collection,
                    fasttext_entity, annoy_index,
                    annoy_index_collection)

    @app.route("/top_people/")
    def top_people():
        return jsonify(top_people=["person1", "person2", "person3"])


    @app.route('/health/', methods=['GET'])
    def health():
        return Response('OK', mimetype='text/plain')

    # @app.route('/banner-rankings', methods=['POST'])
    # def banner_rankings():

    #     data = request.get_json()
    #     valid, error = validate(data)

    #     if not valid:
    #         return error, 400

    #     page_urlpaths = data['pagePaths']
    #     cookie_id = data['cookieId']
    #     enriched = mongo.db['enriched']
    #     return get_most_recent_page_urlpath(enriched, page_urlpaths, cookie_id)
