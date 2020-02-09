"""Default configuration

Use env var to override
"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".flaskenv"))

VERSION = os.getenv("VERSION")
ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
TEST = ENV == "testing"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES"))

ADMIN_ROLE_ID = 1
