import os


class Config:
    DEBUG = False
    TESTING = False


class Development(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/stream_sandbox'


class Testing(Config):
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/cerebroTestDatabase'


class Production(Config):
    MONGO_URI = os.getenv('MONGO_URI')


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
