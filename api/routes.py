from celery import Celery
from flask import request, Response, jsonify, render_template
from quote_attribution_pipeline import quote_attribution
from mongo_collections import (
    annoy_index_collection,
    entity_keywords_collection,
    quote_collection
)
from queries import get_detail, get_search_results


def init_app(app, annoy_index, fasttext_entity):

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    @celery.task
    def quote_attribution_pipeline():
        quote_attribution()

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
        quote_attribution_pipeline.delay()
        return Response("QuoteAttribution", mimetype="text/plain")

    @app.route("/top_people/")
    def top_people():
        return jsonify(top_people=["person1", "person2", "person3"])

    @app.route('/health/', methods=['GET'])
    def health():
        return Response('OK', mimetype='text/plain')
