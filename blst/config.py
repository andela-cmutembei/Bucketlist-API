import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'APP_PRODUCTION_DATABASE_URI'
    )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blst.db')


class TestingConfig(Config):
    TESTING = True
    if os.getenv('TRAVIS_BUILD', None):
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///'


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': ProductionConfig,
}
