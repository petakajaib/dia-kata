from flask import Flask
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from flask_config import app_config
from . import routes


def create_app(environment):

    app = Flask(__name__, instance_relative_config=True)
    handler = RotatingFileHandler(
        "logs/api.log",
        maxBytes=512*1024*1024,
        backupCount=10)
    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    app.config.from_object(app_config[environment])
    app.logger.addHandler(handler)
    app.logger.addHandler(stream_handler)
    CORS(app)
    routes.init_app(app)

    return app
