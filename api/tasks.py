from celery import Celery


def init_app(app):

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    @celery.task
    def quote_attribution_pipeline(self)