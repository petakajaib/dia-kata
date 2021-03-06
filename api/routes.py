from annoy import AnnoyIndex
from flask import request, Response, jsonify, render_template
from gensim.models.fasttext import FastText
from quote_attribution_pipeline import quote_attribution
from mongo_collections import (
    annoy_index_collection,
    entity_keywords_collection,
    quote_collection
)
from queries import get_detail, get_search_results
from settings import ANNOY_INDEX_PATH, FASTTEXT_ENTITY


def init_app(app):

    dimension = 100
    annoy_index = AnnoyIndex(dimension)
    annoy_index.load(ANNOY_INDEX_PATH)
    fasttext_entity = FastText.load(FASTTEXT_ENTITY)

    @app.route("/", methods=['GET'])
    def front_page():
        return render_template("search.html")

    @app.route("/search/", methods=['POST'])
    def search():

        request_body = request.get_json()

        return get_search_results(
                    request_body, fasttext_entity,
                    annoy_index, annoy_index_collection)

    @app.route("/detail/", methods=['POST'])
    def detail():

        request_body = request.get_json()

        return get_detail(
                    request_body, quote_collection,
                    entity_keywords_collection,
                    fasttext_entity, annoy_index,
                    annoy_index_collection)

    @app.route("/top_people/")
    def top_people():
        return jsonify(top_people=["person1", "person2", "person3"])

    @app.route('/health/', methods=['GET'])
    def health():
        return Response('OK', mimetype='text/plain')
