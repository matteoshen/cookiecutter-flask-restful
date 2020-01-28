"""Default configuration

Use env var to override
"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.flaskenv'))

VERSION = os.getenv("VERSION")
ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
JWT_ACCESS_TOKEN_EXPIRES = 3600
{%- if cookiecutter.use_celery == "yes" %}
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND_URL")
{%- endif %}
