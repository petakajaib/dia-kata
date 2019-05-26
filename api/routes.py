from celery import Celery
from annoy import AnnoyIndex
from flask import request, Response, jsonify, render_template, g
from gensim.models.fasttext import FastText
from quote_attribution_pipeline import quote_attribution
from mongo_collections import (
    annoy_index_collection,
    entity_keywords_collection,
    quote_collection
)
from queries import get_detail, get_search_results
from settings import ANNOY_INDEX_PATH, FASTTEXT_ENTITY


def get_some_var():
    some_var = getattr(g, 'some_var', 0)
    return some_var


def add_some_var():
    some_var = get_some_var()
    setattr(g, 'some_var', some_var+2)


def init_app(app):

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    dimension = 100
    annoy_index = AnnoyIndex(dimension)
    annoy_index.load(ANNOY_INDEX_PATH)
    fasttext_entity = FastText.load(FASTTEXT_ENTITY)


    @celery.task
    def quote_attribution_pipeline():
        app.logger.info("quote attribution")
        with app.app_context():
            quote_attribution(logger=app.logger)


    @app.route("/add_2/", methods=["GET"])
    def add_2():

        add_some_var()
        some_var = get_some_var()
        return Response(
                "current val {}".format(some_var),
                mimetype="text/plain")

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

    @app.route("/ftqa/", methods=["GET"])
    def ftqa():
        task = quote_attribution_pipeline.delay()

        print(task.id)
        return Response("QuoteAttribution", mimetype="text/plain")

    @app.route("/top_people/")
    def top_people():
        return jsonify(top_people=["person1", "person2", "person3"])

    @app.route('/health/', methods=['GET'])
    def health():
        return Response('OK', mimetype='text/plain')
