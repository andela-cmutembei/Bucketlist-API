import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET')


# configuration for when in production
class ProductionConfig(Config):
    DEBUG = False


# configuration for when in development
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


# configuration for when testing
class TestingConfig(Config):
    TESTING = True
    if os.getenv('TRAVIS_BUILD', None):
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['TEST_DB_URL']


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': ProductionConfig,
}