import os
from setuptools import setup, find_packages
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(filename='.flaskenv'))

setup(
    name="{{cookiecutter.app_name}}",
    version=os.getenv('VERSION'),
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-restful",
        "flask-migrate",
        "flask-jwt-extended",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        "python-dotenv",
        "passlib",
        "apispec[yaml]",
        "apispec-webframeworks",
        "pymysql",
    ],
    entry_points={
        "console_scripts": [
            "{{cookiecutter.app_name}} = {{cookiecutter.app_name}}.manage:cli"
        ]
    },
)
