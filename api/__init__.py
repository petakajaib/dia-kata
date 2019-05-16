from flask_api import FlaskAPI
from flask_cors import CORS
from logging.handlers import RotatingFileHandler
from flask_config import app_config
from . import routes


def create_app(environment):
    app = FlaskAPI(__name__, instance_relative_config=True)
    handler = RotatingFileHandler(
        "logs/api.log",
        maxBytes=512*1024*1024,
        backupCount=10)
    app.config.from_object(app_config[environment])
    app.logger.addHandler(handler)
    CORS(app)
    routes.init_app(app)
    return app
