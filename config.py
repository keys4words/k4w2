import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'asldkjfiu4304jfajfjPJF_DJ$EJsdfadf43343s'


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    SECRET_KEY = 'asldkjfiu4304jfajfjPJF_DJ$EJsdfadf43343s'
    SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_password@db-postgres:5432/flask-deploy'
    CELERY_BROKER = 'pyamqp://rabbit_user:rabbit_password@broker-rabbitmq//'
    CELERY_RESULT_BACKEND = 'rpc://rabbit_user:rabbit_password@broker-rabbitmq//'


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    DEBUG = False
    SECRET_KEY = 'asldkjfiu4304jfajfjPJF_DJ$EJsdfadf43343s'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'db.sqlite')


class TestConfig(BaseConfig):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    CELERY_ALWAYS_EAGER = True



