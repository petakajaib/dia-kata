import os


class Config:
    DEBUG = False
    TESTING = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

class Development(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/stream_sandbox'


class Testing(Config):
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/cerebroTestDatabase'


class Staging(Config):
    DEBUG = True
    TESTING = True


class Production(Config):
    MONGO_URI = os.getenv('MONGO_URI')


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'staging': Staging
}
