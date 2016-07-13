import os
from flask.ext.dotenv import DotEnv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
    """Main configuration class"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET')

    @classmethod
    def init_app(self, app):
        env = DotEnv()
        env.init_app(app, os.path.join(BASE_DIR, '.env'), verbose_mode=True)


# configuration for when in production
class ProductionConfig(Config):
    """configuration for when in production"""
    DEBUG = False


# configuration for when in development
class DevelopmentConfig(Config):
    """configuration for when in development"""
    DEVELOPMENT = True
    DEBUG = True


# configuration for when testing
class TestingConfig(Config):
    """configuration for when testing"""
    TESTING = True
    if os.getenv('TRAVIS_BUILD', None):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URL')


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': ProductionConfig,
}
