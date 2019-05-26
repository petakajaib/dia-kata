from flask import Flask
from annoy import AnnoyIndex
from flask_cors import CORS
from gensim.models.fasttext import FastText
import logging
from logging.handlers import RotatingFileHandler, StreamHandler
from flask_config import app_config
from settings import (
    ANNOY_INDEX_PATH,
    FASTTEXT_ENTITY
)
from . import routes


def create_app(environment):

    dimension = 100
    annoy_index = AnnoyIndex(dimension)
    annoy_index.load(ANNOY_INDEX_PATH)
    fasttext_entity = FastText.load(FASTTEXT_ENTITY)

    app = Flask(__name__, instance_relative_config=True)
    handler = RotatingFileHandler(
        "logs/api.log",
        maxBytes=512*1024*1024,
        backupCount=10)
    stream_handler = StreamHandler()
    stream_handler.set_level(logging.DEBUG)
    app.config.from_object(app_config[environment])
    app.logger.addHandler(handler)
    app.logger.addHandler(stream_handler)
    CORS(app)
    routes.init_app(app, annoy_index, fasttext_entity)

    return app
